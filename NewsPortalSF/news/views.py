
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .filters import PostFilter


class Posts(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context



class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    template_name = 'post_create.html'



class PostEdit(UpdateView):
    model = Post
    template_name = 'news/post_create.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/deletepost.html'
    context_object_name = 'deletenews'