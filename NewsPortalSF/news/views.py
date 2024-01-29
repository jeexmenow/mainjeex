from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import Post, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.core.paginator import Paginator
from django_filters.views import FilterView
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from django.views import View

class PostsList(ListView):
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


class PostCreate(PermissionRequiredMixin, CreateView):
    template_name = 'create_for_user.html'
    form_class = PostForm
    permission_required = ('news.add_post',
                           'news.change_post')


def add_post(request):
    if not request.user.has_perm('news.add_post', 'news.change_post'):
        raise PermissionDenied


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post',
                           'news.change_post')

    def change_post(request):
        if not request.user.has_perm('News.add_post', 'News.change_post'):
            raise PermissionDenied

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get(self, request):
        printer.apply_async([10], countdown = 5)
        hello.delay()
        return HttpResponse('Hello!')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class CategoryListView(PostsList):
    model = Post
    template_name = 'subscribers/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'],)
        queryset = Post.objects.filter(categories=self.category).order_by('-created_time')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribers/subscribe.html', {'category': category, 'message': message})
