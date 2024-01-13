from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return self.user.username

    def update_rating(self):
        post_rating = Post.objects.filter(author=self).aggregate(
            Sum('rating'))['rating__sum']
        comment_rating = Comment.objects.filter(user=self.user).aggregate(
            Sum('rating'))['rating__sum']
        comment_rating_to_posts = Comment.objects.filter(
            post__author__user=self.user).aggregate(Sum('rating'))[
            'rating__sum']

        self.rating = ((post_rating * 3) + comment_rating +
                       comment_rating_to_posts)
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name



class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, choices=[
        ('статья', 'Статья'), ('новость', 'Новость')])
    created_time = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory',
                                        related_name='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title} {self.text}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'

    def __str__(self):
        return f'id-{self.pk}: {self.title}'




class PostCategory(models.Model):
    postTrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryTrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()