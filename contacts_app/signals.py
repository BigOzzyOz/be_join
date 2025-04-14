import logging
from django.db.models.signals import pre_delete, post_save
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
    update_fields = kwargs.get("update_fields")
    if update_fields is not None and "name" not in update_fields:
        if "profile_pic" not in update_fields and "first_letters" not in update_fields:
            return

    try:
        orig_first_letters = instance.first_letters
        orig_profile_pic = instance.profile_pic

        new_letters = get_initials_from_name(instance.name)
        new_pic = ""

        fields_to_update_dict = {}

        if orig_first_letters != new_letters:
            fields_to_update_dict["first_letters"] = new_letters
            new_pic = generate_svg_circle_with_initials(instance.name)
            if orig_profile_pic != new_pic:
                fields_to_update_dict["profile_pic"] = new_pic if new_pic else ""

        elif (not orig_profile_pic or orig_profile_pic.isspace()) and (
            update_fields is None or "profile_pic" not in update_fields
        ):
            new_pic = generate_svg_circle_with_initials(instance.name)
            if new_pic and not new_pic.isspace():
                fields_to_update_dict["profile_pic"] = new_pic

        if fields_to_update_dict:
            rows_updated = sender._base_manager.filter(pk=instance.pk).update(**fields_to_update_dict)

            if rows_updated > 0:
                for field, value in fields_to_update_dict.items():
                    setattr(instance, field, value)
                logger.info(f"Updated visuals for contact {instance.pk} in post_save signal.")

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
