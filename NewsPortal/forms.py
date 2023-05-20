from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Post


class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['categories', 'title', 'text']
