from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from Project import settings
from .models import Post, Category


def send_emails(subject, html_content, emails, from_email=settings.EMAIL_HOST_USER):
    msg = EmailMultiAlternatives(subject=subject, from_email=from_email, to=emails)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_sub_notifications(pk, user_emails):
    post = Post.objects.get(pk=pk)
    context = {
        "title": post.title,
        "text": post.preview(),
        "url": post.get_post_url(),
    }
    email_title = f"Новая статья на сайте, читайте о: {post.title}"

    template = 'emails/subscribed_category_notification_email.html'
    html_content = render_to_string(template, context)

    send_emails(email_title, html_content, user_emails)


@shared_task
def send_welcome_notification(user_email):
    email_title = f"Welcome message from {settings.SITE_URL}"
    template = 'emails/welcome_email_notification.html'
    html_content = render_to_string(template)

    send_emails(email_title, html_content, user_email)


@shared_task
def send_best_weekly_posts(users_emails=Category.get_all_users_emails()):
    best_weekly_posts = Post.get_best_posts_in_last_week()
    context = {
        'posts': best_weekly_posts,
    }
    email_title = f'Best weekly'

    template = 'emails/best_weekly_posts_email.html'
    html_content = render_to_string(template, context)
    send_emails(email_title, html_content, users_emails)


