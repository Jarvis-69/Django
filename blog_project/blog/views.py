# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

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

def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Vérifier si l'utilisateur connecté est l'auteur du post
    if post.author != request.user:
        return redirect('post_list')  # Redirige vers la liste des posts si l'utilisateur n'est pas l'auteur

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)  # Redirige vers la page de détails du post
    else:
        form = PostForm(instance=post)
    
    return render(request, 'edit_post.html', {'form': form, 'post': post})

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')  # Rediriger après suppression

    return render(request, 'confirm_delete.html', {'post': post})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Récupérer l'utilisateur et le connecter
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')  # Rediriger vers la liste des posts
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('post_list')

