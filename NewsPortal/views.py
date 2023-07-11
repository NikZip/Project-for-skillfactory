from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# debug
from .tasks import *
from Project import settings


from .models import Post, Author, Category
from .filters import PostFilter
from .forms import NewsForm


class NewsList(ListView):
    model = Post
    ordering = '-creation_date'
    template_name = 'NewsPortal/homepage.html'
    context_object_name = 'posts'
    paginate_by = 10


class NewsSearch(NewsList):
    template_name = 'NewsPortal/search.html'

    def get_queryset(self):
        queryset = Post.objects.all().order_by(self.ordering)
        queryset = PostFilter(self.request.GET, queryset=queryset).qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET)
        return context


class NewsDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'NewsPortal/detail_news.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'NewsPortal.add_post'
    model = Post
    form_class = NewsForm
    template_name = 'NewsPortal/edit.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form, **kwargs):
        post = form.save(commit=False)
        post.author = Author.objects.get(user_id=self.request.user.id)
        post.post_type = self.kwargs['post_type']
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'NewsPortal.change_post'
    model = Post
    form_class = NewsForm
    template_name = 'NewsPortal/edit.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form, **kwargs):
        post = form.save(commit=False)
        post.post_type = self.kwargs['post_type']
        return super().form_valid(form)


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'NewsPortal.delete_post'
    model = Post
    template_name = 'NewsPortal/delete.html'
    success_url = reverse_lazy('posts_list')


@login_required
def make_author(request):
    if not request.user.groups.filter(name='author').exists():
        user = request.user

        author_group = Group.objects.get(name='author')
        author_group.user_set.add(user)

        author = Author.objects.create(user=user)
        author.save()

        messages.info(request, 'Author created successfully')
        return redirect('posts_list')
    else:
        messages.info(request, 'You have no access to this page')
        return redirect('posts_list')


#  Profiles
class ProfileView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'NewsPortal/profile.html'


def subscribe(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.subscribers.add(request.user)
    category.save()
    messages.info(request, f'Successfully subscribed to {category}')
    return redirect('user_profile')


def unsubscribe(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.subscribers.remove(request.user)
    category.save()
    messages.info(request, f'Successfully unsubscribed of {category}')
    return redirect('user_profile')


#  Debugging
class DebugView(ListView):
    model = Category
    template_name = 'NewsPortal/debug.html'


def debug_send_sub_email(request):
    debug_email = [settings.EMAIL_DEBUG]
    first_post = Post.objects.all().first()
    send_sub_notifications.apply_async(args=[first_post.pk, debug_email], countdown=0)
    return redirect('debug')


def debug_send_welcome_notification(request):
    debug_email = [settings.EMAIL_DEBUG]
    send_welcome_notification.apply_async(args=[debug_email], countdown=0)
    return redirect('debug')


def debug_send_best_weekly_posts(request):
    debug_email = [settings.EMAIL_DEBUG]
    send_best_weekly_posts.apply_async(args=[debug_email], countdown=0)
    return redirect('debug')