# blog/views.py
from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

def post_list(request):
    # Récupérer tous les posts, en filtrant pour ceux qui sont publiés
    posts = Post.objects.filter(status='published').order_by('-created_at')

    # Retourner un rendu de la template 'post_list.html', en passant les posts
    return render(request, 'blog/post_list.html', {'posts': posts})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()  # Sauvegarde directement avec l'auteur sélectionné
            return redirect('post_list')  # Redirige vers la liste des articles
    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {'form': form})


