from django import forms
from .models import Post, Category
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']
        labels = {
            'title': _('Titre'),
            'content': _('Contenu'),
            'category': _('Catégorie'),
            'image': _('Image')
        }

    # Champ catégorie avec la traduction de l'erreur
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label=_('Catégorie'),
        error_messages={'required': _('Veuillez sélectionner une catégorie.')}
    )
