import logging
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from contacts_app.models import Contact
from contacts_app.utils import generate_svg_circle_with_initials

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_or_update_contact(sender, instance, created, **kwargs):
    try:
        if created:
            contact = Contact.objects.filter(email=instance.email).first()
            if contact:
                contact.user = instance
                contact.name = (
                    f"{instance.first_name} {instance.last_name}"
                    if instance.first_name or instance.last_name
                    else instance.username
                )
                contact.first_letters = "".join(
                    [name[0].upper() for name in f"{instance.first_name} {instance.last_name}".split() if name]
                )
                contact.profile_pic = generate_svg_circle_with_initials(f"{instance.first_name} {instance.last_name}")
                contact.is_user = True
                contact.save()
            else:
                Contact.objects.create(
                    email=instance.email,
                    name=f"{instance.first_name} {instance.last_name}"
                    if instance.first_name or instance.last_name
                    else instance.username,
                    number="Please add your number",
                    first_letters="".join(
                        [name[0].upper() for name in f"{instance.first_name} {instance.last_name}".split() if name]
                    ),
                    is_user=True,
                    profile_pic=generate_svg_circle_with_initials(f"{instance.first_name} {instance.last_name}"),
                    user=instance,
                )
        else:
            contact = Contact.objects.filter(user=instance).first()
            if contact:
                contact.email = instance.email
                contact.name = f"{instance.first_name} {instance.last_name}"
                contact.first_letters = "".join(
                    [name[0].upper() for name in f"{instance.first_name} {instance.last_name}".split() if name]
                )
                contact.profile_pic = generate_svg_circle_with_initials(f"{instance.first_name} {instance.last_name}")
                contact.save()
    except Exception as e:
        logger.error(f"Error in create_or_update_contact signal: {e}")


@receiver(pre_delete, sender=User)
def delete_user_tag_in_contact(sender, instance, **kwargs):
    try:
        contact = Contact.objects.filter(user=instance).first()
        if contact:
            contact.user = None
            contact.is_user = False
            contact.save()
    except Exception as e:
        logger.error(f"Error in delete_user_tag_in_contact signal: {e}")
