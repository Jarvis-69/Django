from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Post, Category
from django.core.exceptions import PermissionDenied

# Créer un groupe avec des permissions personnalisées
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Vérifier si l'utilisateur appartient à un groupe spécifique
        if request.user.groups.filter(name="Administrateurs").exists():
            # Si l'utilisateur est un modérateur, il peut modifier n'importe quelle publication
            obj.save()
        else:
            # Sinon, il peut modifier uniquement ses propres publications
            if obj.author == request.user:
                obj.save()
            else:
                raise PermissionDenied("Vous n'êtes pas autorisé à modifier cette publication.")

admin.site.register(Category)
