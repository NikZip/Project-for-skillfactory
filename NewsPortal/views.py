from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Post, Author
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


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'NewsPortal.add_post'
    model = Post
    form_class = NewsForm
    template_name = 'NewsPortal/edit.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form, **kwargs):
        post = form.save(commit=False)
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
        return HttpResponseRedirect('/')
    else:
        messages.info(request, 'You have no access to this page')
        return HttpResponseRedirect('/')
