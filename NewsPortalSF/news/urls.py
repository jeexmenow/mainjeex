from django.urls import path
from . views import Posts, PostDetail, PostCreate, SearchNews, PostDeleteView, PostUpdateView


urlpatterns = [
    path('', Posts.as_view(), name='post_list'),
    path('search/', SearchNews.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_full'),
    path('create/', PostCreate.as_view(), name='newpost'),
    path('create/<int:pk>', PostUpdateView.as_view(), name='post_create'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    ]