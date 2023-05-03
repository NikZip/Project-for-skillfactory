from django.views.generic import ListView, DetailView
from .models import *


class NewsList(ListView):
    model = Post
    ordering = '-creation_date'
    template_name = 'news.html'
    context_object_name = 'posts'


class NewsDetail(DetailView):
    model = Post
    template_name = 'article.html'
    context_object_name = 'post'



