
from .models import Post, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.core.paginator import Paginator
from django_filters.views import FilterView
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView


class Posts(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-created_time'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 5

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


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
    template_name = 'post_full.html'
    queryset = Post.objects.all()

class SearchNews(FilterView):
    model = Post
    filterset_class = PostFilter
    template_name = 'search.html'
    paginate_by = 10
    context_object_name = 'news'


class PostCreate(CreateView, PermissionRequiredMixin, LoginRequiredMixin):
    template_name = 'create_for_user.html'
    form_class = PostForm
    permission_required = ('Models.add_post',
                           'Models.change_post')

class PostUpdateView(UpdateView, PermissionRequiredMixin, LoginRequiredMixin):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('Models.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)



class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'




