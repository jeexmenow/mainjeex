from django.urls import path
from .views import PostsList, PostDetail, PostCreate, SearchNews, PostDeleteView, PostUpdateView, CategoryListView, \
    subscribe, IndexView
from django.urls import path, include
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('search/', SearchNews.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_full'),
    path('add/', PostCreate.as_view(), name='newpost'),
    path('edit/<int:pk>', PostUpdateView.as_view(), name='post_create'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('', include('protect.urls')),
    path('sign/', include('sign.urls')),
    path('accounts/', include('allauth.urls')),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribers', subscribe, name='subscribers'),
    path('', IndexView.as_view()),
    path('<int:pk>/', cache_page(60*10)(PostDetail.as_view()), name='product_detail'),
]

