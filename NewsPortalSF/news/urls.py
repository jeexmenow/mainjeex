from django.urls import path
from .views import Posts, PostDetail, PostCreate, SearchNews, PostDeleteView, PostUpdateView, CategoryListView, \
    subscribe
from django.urls import path, include

urlpatterns = [
    path('', Posts.as_view(), name='post_list'),
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
]

