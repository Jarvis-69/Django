from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

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

class Post(models.Model):    
    STATUS_CHOICES = (        
        ('draft', 'Draft'),        
        ('published', 'Published')    
    )    
    
    title = models.CharField(max_length=200)    
    slug = models.SlugField(unique=True)    
    content = models.TextField()     
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)  # Valeur par défaut pour les nouveaux posts
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')    
    image = models.ImageField(upload_to='blog_images/%Y/%m/%d/', blank=True)    
    # tags = models.ManyToManyField('Tag', blank=True)