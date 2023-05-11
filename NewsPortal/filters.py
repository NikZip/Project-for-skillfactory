from django import forms
from django_filters import FilterSet, DateFilter, CharFilter
from .models import Post


class PostFilter(FilterSet):
    text_query = CharFilter(field_name='title', lookup_expr='icontains')
    author_name = CharFilter(field_name='author__user__username', lookup_expr='icontains')
    creation_date = DateFilter(field_name='creation_date',
                               widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                               lookup_expr='lt')

    class Meta:
        model = Post
        fields = ['text_query', 'author_name', 'creation_date']

