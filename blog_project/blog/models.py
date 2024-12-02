from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ('name',)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_detail', args=[self.slug])
    

class Author(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création de l'auteur

    def __str__(self):
        return self.name


class Post(models.Model):    
    STATUS_CHOICES = (        
        ('draft', 'Draft'),        
        ('published', 'Published')    
    )    
    
    title = models.CharField(max_length=200)    
    slug = models.SlugField(unique=True, blank=True)    
    content = models.TextField()     
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)  # Valeur par défaut pour les nouveaux posts
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')    
    image = models.ImageField(upload_to='blog_images/%Y/%m/%d/', blank=True)  
    # tags = models.ManyToManyField('Tag', blank=True)

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