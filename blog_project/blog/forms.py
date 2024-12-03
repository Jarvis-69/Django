from django import forms
from .models import Post, Category
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']
        labels = {
            'title': 'Titre',
            'content': 'Contenu',
            'category': 'Catégorie',
            'image': 'Image'
        }

    # Champ catégorie (comme avant)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)