import logging
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from contacts_app.models import Contact
from contacts_app.utils import generate_svg_circle_with_initials, get_initials_from_name

logger = logging.getLogger(__name__)


def _calculate_contact_attributes(instance):
    full_name = f"{instance.first_name} {instance.last_name}".strip()
    contact_name = full_name if full_name else instance.username
    first_letters = get_initials_from_name(contact_name)
    profile_pic = generate_svg_circle_with_initials(contact_name)
    return contact_name, first_letters, profile_pic


def _update_existing_contact(contact, instance, contact_name, first_letters, profile_pic):
    contact.email = instance.email
    contact.name = contact_name
    contact.first_letters = first_letters
    contact.profile_pic = profile_pic
    contact.save(update_fields=["email", "name", "first_letters", "profile_pic"])


def _update_contact_found_by_email(contact, instance, contact_name, first_letters, profile_pic):
    contact.user = instance
    contact.name = contact_name
    contact.first_letters = first_letters
    contact.profile_pic = profile_pic
    contact.is_user = True
    contact.save(update_fields=["user", "name", "first_letters", "profile_pic", "is_user"])


@receiver(post_save, sender=User)
def create_or_update_contact(sender, instance, created, **kwargs):
    try:
        name, letters, pic = _calculate_contact_attributes(instance)
        if created:
            contact, was_created = _get_or_create_contact(instance, name, letters, pic)
            if not was_created:
                _update_contact_found_by_email(contact, instance, name, letters, pic)
        else:
            _update_contact_if_exists(instance, name, letters, pic)
    except Exception as e:
        logger.error(f"Error in signal for user {instance.username}: {e}")

def _get_or_create_contact(instance, name, letters, pic):
    return Contact.objects.get_or_create(
        email=instance.email,
        defaults={
            "name": name,
            "number": "Please add your number",
            "first_letters": letters,
            "profile_pic": pic,
            "is_user": True,
            "user": instance,
        },
    )

def _update_contact_if_exists(instance, name, letters, pic):
    contact = Contact.objects.filter(user=instance).first()
    if contact:
        _update_existing_contact(contact, instance, name, letters, pic)


@receiver(pre_delete, sender=User)
def delete_user_tag_in_contact(sender, instance, **kwargs):
    try:
        updated_count = Contact.objects.filter(user=instance).update(user=None, is_user=False)
        if updated_count == 0:
            logger.info(f"No contact found for user {instance.username} during deletion.")
    except Exception as e:
        logger.error(f"Error in pre_delete signal for user {instance.username}: {e}")
