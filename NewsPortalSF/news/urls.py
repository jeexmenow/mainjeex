from django.urls import path
from . views import Posts, PostDetail, PostCreate, SearchNews


urlpatterns = [
    path('', Posts.as_view(), name='post_list'),
    path('search/', SearchNews.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create', PostCreate.as_view(), name='newpost'),
    ]