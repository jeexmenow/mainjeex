import django.forms
from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import Post, Author




class PostFilter(FilterSet):
    created_time = DateFilter(lookup_expr='gt', widget=django.forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    title = CharFilter(
        lookup_expr='icontains',
        widget=django.forms.TextInput(
            attrs={'type': 'text',
                   'class': 'form-control',
                   'placeholder': 'Enter title',
                   'name': 'title'
                   }
        )
    )
    text = CharFilter(
        lookup_expr='icontains',
        widget=django.forms.TextInput(
            attrs={'type': 'text',
                   'class': 'form-control'
                   }
        )
    )

    author = ModelChoiceFilter(
        label ='Автор',
        empty_label='Все авторы',
        queryset=Author.objects.all(),
        widget=django.forms.Select(attrs={'class': 'form-control'})
    )






    class Meta:
        model = Post
        fields = []

