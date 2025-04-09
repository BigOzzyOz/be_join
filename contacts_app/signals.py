import logging
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Contact


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Contact)
def create_update_contact_profile(sender, instance, created, **kwargs):
    try:
        if not created and instance.is_user and instance.user:
            # Aktualisiere nur die Felder, die sich geändert haben
            updates = {}
            if instance.email != instance.user.email:
                updates["email"] = instance.email
            if instance.name != f"{instance.user.first_name} {instance.user.last_name}":
                name_parts = instance.name.split(" ", 1)
                updates["first_name"] = name_parts[0]
                updates["last_name"] = name_parts[1] if len(name_parts) > 1 else ""

            if updates:
                User.objects.filter(pk=instance.user.pk).update(**updates)

    except Exception as e:
        logger.error(f"Error creating/updating contact profile: {e}")


@receiver(pre_delete, sender=Contact)
def delete_contact_profile(sender, instance, **kwargs):
    try:
        if instance.is_user:
            user = instance.user
            if user:
                user.delete()
    except Exception as e:
        logger.error(f"Error deleting contact profile: {e}")
