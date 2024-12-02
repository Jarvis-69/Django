from django import forms
from .models import Post, Category
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'status', 'category', 'image', 'author']

    # Champ catégorie (comme avant)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)

    # Champ auteur, permettant de choisir parmi tous les utilisateurs
    author = forms.ModelChoiceField(queryset=User.objects.all(), required=True, empty_label="Choose an author")