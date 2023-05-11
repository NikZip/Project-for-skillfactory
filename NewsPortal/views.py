from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post
from .filters import PostFilter
from .forms import NewsForm


class NewsList(ListView):
    model = Post
    ordering = '-creation_date'
    template_name = 'homepage.html'
    context_object_name = 'posts'
    paginate_by = 10


class NewsSearch(NewsList):

    template_name = 'search.html'

    def get_queryset(self):
        queryset = Post.objects.all().order_by(self.ordering)
        queryset = PostFilter(self.request.GET, queryset=queryset).qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET)
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'detail_news.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    model = Post
    form_class = NewsForm
    template_name = 'edit.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form, **kwargs):
        post = form.save(commit=False)
        post.post_type = self.kwargs['post_type']
        return super().form_valid(form)


class PostUpdate(UpdateView):
    model = Post
    form_class = NewsForm
    template_name = 'edit.html'
    success_url = reverse_lazy('posts_list')

    def form_valid(self, form, **kwargs):
        post = form.save(commit=False)
        post.post_type = self.kwargs['post_type']
        return super().form_valid(form)


class PostDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('posts_list')


