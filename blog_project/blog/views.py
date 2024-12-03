# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from .forms import PostForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def post_list(request):
    # Récupérer tous les posts, en filtrant pour ceux qui sont publiés
    posts = Post.objects.all().order_by('-created_at')
    is_admin = request.user.groups.filter(name="Administrateurs").exists()

     # Filtrer par catégorie
    category_filter = request.GET.get('category')  # Récupérer la catégorie depuis les paramètres GET
    if category_filter:
        posts = posts.filter(category__name=category_filter)

    # Filtrer par utilisateur
    user_filter = request.GET.get('user')  # Récupérer l'utilisateur depuis les paramètres GET
    if user_filter:
        posts = posts.filter(author__username=user_filter)

    categories = Category.objects.all()  # Récupérer toutes les catégories
    users = User.objects.all()  # Récupérer tous les utilisateurs (ou personnaliser selon vos besoins)

    context = {
        'posts': posts,
        'categories': categories,
        'users': users,
        'user': request.user,
        'is_admin': is_admin
    }

    # Retourner un rendu de la template 'post_list.html', en passant les posts
    return render(request, 'blog/post_list.html', context)

@login_required  # Assure que l'utilisateur soit connecté avant de pouvoir créer un post
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # Ne pas sauvegarder immédiatement
            post.author = request.user  # Associer l'utilisateur connecté comme auteur
            post.save()  # Sauvegarder l'article
            return redirect('post_list')  # Rediriger vers la liste des posts après la création
    else:
        form = PostForm()
    
    return render(request, 'blog/create_post.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

def edit_post(request, pk):
    # Récupérer le post avec le pk passé dans l'URL
    post = get_object_or_404(Post, pk=pk)

    # Si la requête est en POST, mettre à jour les informations du post
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()  # Sauvegarde le post modifié
            return redirect('post_list')  # Redirection vers la liste des posts
    else:
        form = PostForm(instance=post)  # Si c'est un GET, afficher le formulaire pré-rempli avec les données actuelles du post

    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        post.delete()
        return redirect('post_list')  # Redirige vers la liste des posts après la suppression
    return render(request, 'blog/confirm_delete.html', {'post': post})

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

