from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from numpy import unique

from Project import settings


class RatingSystem(models.Model):
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    class Meta:
        abstract = True


class Author(RatingSystem):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        posts = Post.objects.filter(author=self)
        comments = Comment.objects.filter(user=self.user)

        posts_rating = 0
        comments_rating = 0

        for post in posts:
            posts_rating += post.rating * 3

        for comment in comments:
            comments_rating += comment.rating

        total_rating = posts_rating + comments_rating
        self.rating += total_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    @staticmethod
    def get_all_users_emails():
        non_duplicated_emails = Category.get_emails_from_queryset(Category.objects.all())
        return non_duplicated_emails

    @staticmethod
    def get_emails_from_queryset(queryset):
        all_emails = []
        for category in queryset:
            all_emails += category.get_subs_emails()

        non_duplicated_emails = list(unique(all_emails))
        return non_duplicated_emails

    def get_subs_emails(self):
        subscribers = self.subscribers.all()
        subscribers_emails = [sub.email for sub in subscribers]
        return subscribers_emails

    def __str__(self):
        return self.name


class Post(RatingSystem):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    type_choices = (('news', 'news'), ('article', 'article'))
    post_type = models.CharField(max_length=7, choices=type_choices, blank=False, null=False)

    creation_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=100)
    text = models.TextField()

    @staticmethod
    def get_best_posts_in_last_week():
        start_date = timezone.now().date() - timedelta(days=7)
        end_date = timezone.now().date()
        top_10 = 10
        return list(Post.objects.filter(creation_date__gte=start_date,
                                        creation_date__lt=end_date).order_by('-rating')[:top_10])

    def get_post_url(self):
        post_url = reverse('post_detail', kwargs={'pk': self.pk})
        site_url = settings.SITE_URL
        return f'{site_url}{post_url}'

    def preview(self):
        prev_text_amount = 124
        return self.text[:prev_text_amount] + '...'

    def get_post_author(self):
        return self.author.user


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(RatingSystem):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
