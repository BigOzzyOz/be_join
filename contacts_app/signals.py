import logging
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Contact
from .utils import get_initials_from_name, generate_svg_circle_with_initials

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Contact)
def create_update_contact_profile(sender, instance, created, **kwargs):
    try:
        if not created and instance.is_user and instance.user:
            updates = {}
            if instance.email != instance.user.email:
                updates["email"] = instance.email
            if instance.name != f"{instance.user.first_name} {instance.user.last_name}".strip():
                name_parts = instance.name.split(" ", 1)
                updates["first_name"] = name_parts[0]
                updates["last_name"] = name_parts[1] if len(name_parts) > 1 else ""

            if updates:
                User.objects.filter(pk=instance.user.pk).update(**updates)

    except Exception as e:
        logger.error(f"Error creating/updating contact profile: {e}")


@receiver(post_save, sender=Contact)
def update_contact_visuals(sender, instance, created, **kwargs):
    try:
        current_instance = Contact.objects.get(pk=instance.pk)

        new_letters = get_initials_from_name(current_instance.name)
        update_fields = []

        old_profile_pic = current_instance.profile_pic

        if current_instance.first_letters != new_letters:
            current_instance.first_letters = new_letters
            update_fields.append("first_letters")

            new_pic = generate_svg_circle_with_initials(current_instance.name)
            current_instance.profile_pic = new_pic if new_pic else ""
            if old_profile_pic != current_instance.profile_pic:
                update_fields.append("profile_pic")

        elif old_profile_pic is None or old_profile_pic == "" or old_profile_pic.isspace():
            new_pic = generate_svg_circle_with_initials(current_instance.name)
            current_instance.profile_pic = new_pic if new_pic else ""
            if current_instance.profile_pic and not current_instance.profile_pic.isspace():
                update_fields.append("profile_pic")

        if update_fields:
            current_instance.save(update_fields=update_fields)

    except Contact.DoesNotExist:
        logger.warning(f"Contact {instance.pk} not found when trying to update visuals in post_save signal.")
    except Exception as e:
        logger.error(f"Error updating contact visuals for contact {instance.pk}: {e}", exc_info=True)


@receiver(pre_delete, sender=Contact)
def delete_associated_user(sender, instance, **kwargs):
    try:
        if instance.is_user and instance.user:
            user_to_delete = instance.user
            instance.user = None
            user_to_delete.delete()
            logger.warning(
                f"Deleted user {user_to_delete.username} because associated contact {instance.pk} was deleted."
            )
    except User.DoesNotExist:
        logger.warning(f"User associated with contact {instance.pk} not found during pre_delete.")
    except Exception as e:
        logger.error(f"Error deleting user associated with contact {instance.pk}: {e}")
