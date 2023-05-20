from allauth.account.signals import user_signed_up
from django.contrib.auth.models import Group
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .tasks import send_sub_notifications, send_welcome_notification
from .models import PostCategory, Category


# Task receivers
@receiver(user_signed_up)
def send_welcome_email(**kwargs):
    user = kwargs['user']
    send_welcome_notification.apply_async(args=[[user.email]], countdown=1)


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(instance, **kwargs):
    if kwargs['action'] == 'post_add':
        non_duplicated_emails = Category.get_emails_from_queryset(instance.categories.all())

        send_sub_notifications.apply_async(args=[instance.pk, non_duplicated_emails], countdown=1)


# Events receivers
@receiver(user_signed_up)
def set_group_to_new_user(**kwargs):
    user = kwargs['user']
    common_group = Group.objects.get(name='common')
    user.groups.add(common_group)
