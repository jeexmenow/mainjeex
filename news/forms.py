from django.forms import ModelForm
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['author', 'categories', 'title', 'text']

