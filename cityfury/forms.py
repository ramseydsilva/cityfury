from django import forms
from .models import Post
from django_select2.widgets import *
from .models import *


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption', 'location_string', 'city', 'area', 'category']
