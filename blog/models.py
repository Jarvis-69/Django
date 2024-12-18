from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Post(models.Model):    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True) 
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    image = models.ImageField(upload_to='blog_images/%Y/%m/%d/', blank=True)

    class Meta:
        permissions = [
            ("can_edit_all_posts", "Peut modifier toutes les publications"),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:  # Si le slug n'est pas déjà défini
            self.slug = slugify(self.title)  # Crée le slug à partir du titre
            # Vérifie si le slug existe déjà et ajoute un suffixe si nécessaire
            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title