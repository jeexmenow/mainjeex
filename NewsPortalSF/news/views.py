
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.core.paginator import Paginator
from django_filters.views import FilterView

from .filters import PostFilter


class Posts(ListView):
    model = Post
    ordering = '-created_time'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context



class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class SearchNews(FilterView):
    model = Post
    filterset_class = PostFilter
    template_name = 'search.html'
    paginate_by = 10
    context_object_name = 'news'


class PostCreate(CreateView):
    template_name = 'post_create.html'


class PostEdit(UpdateView):
    model = Post
    template_name = 'news/post_create.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/deletepost.html'
    context_object_name = 'deletenews'