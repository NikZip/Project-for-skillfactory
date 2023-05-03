from django.db import models
from django.contrib.auth.models import User


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
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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


class Post(RatingSystem):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    type_choices = (('news', 'news'), ('article', 'article'))
    post_type = models.CharField(max_length=7, choices=type_choices)

    creation_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=100)
    text = models.TextField()

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

