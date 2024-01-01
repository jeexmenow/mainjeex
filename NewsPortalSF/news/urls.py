from django.urls import path
from . views import Posts, PostDetail, PostCreate


urlpatterns = [
    path('', Posts.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create', PostCreate.as_view(), name='newpost'),
    ]