from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.core.cache import cache

NEWSPAPER = [('Новости', 'Статья')]


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)

    def update_rating(self):
        author_posts_rating = Post.objects.filter(author_id=self.pk).aggregate(r1=Coalesce(Sum('rating'), 0))['r1']
        author_comments_rating = Comment.objects.filter(user_id=self.user).aggregate(r2=Coalesce(Sum('rating'), 0))['r2']
        author_posts_comments_rating = Comment.objects.filter(post__author__user=self.user).aggregate(r3=Coalesce(Sum('rating'), 0))['r3']
        self.rating = (author_posts_rating * 3) + author_comments_rating + author_posts_comments_rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True, null=True)
    subscribers = models.ManyToManyField(User, related_name='categories')


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=255, choices=NEWSPAPER)
    post_datetime = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    header = models.CharField(max_length=255, null=True)
    text = models.TextField(null=True)
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:124]}...'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post_key = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_key = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True)
    comment_datetime = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()