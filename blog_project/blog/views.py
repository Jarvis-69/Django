from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from .forms import PostForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.conf import settings
from django.utils.translation import activate

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    is_admin = request.user.groups.filter(name="Administrateurs").exists()

     # Filtrer par catégorie
    category_filter = request.GET.get('category')
    if category_filter:
        posts = posts.filter(category__name=category_filter)

    # Filtrer par utilisateur
    user_filter = request.GET.get('user')
    if user_filter:
        posts = posts.filter(author__username=user_filter)

    categories = Category.objects.all()
    users = User.objects.all()

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
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
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

from django.utils.translation import activate
from django.shortcuts import redirect
from django.conf import settings

from django.utils.translation import activate
from django.shortcuts import redirect
from django.conf import settings
from urllib.parse import urlparse, urlunparse

from django.utils.translation import activate
from django.shortcuts import redirect
from django.conf import settings
from urllib.parse import urlparse, urlunparse

def set_language(request):
    language = request.GET.get('language')  # Récupérer la langue de la query string
    if language:
        activate(language)  # Activer la langue
        request.session[settings.LANGUAGE_SESSION_KEY] = language  # Stocker la langue dans la session

    # Récupérer l'URL de la page précédente
    referer = request.META.get('HTTP_REFERER', '/')
    
    # Parser l'URL de référence pour en extraire la partie path
    parsed_url = urlparse(referer)
    path = parsed_url.path

    # Vérifier et nettoyer la langue déjà présente dans le chemin (si elle existe)
    if path.startswith('/fr/'):
        path = path[3:]  # Retirer '/fr/' du début du path
    elif path.startswith('/en/'):
        path = path[3:]  # Retirer '/en/' du début du path

    # Ajouter la nouvelle langue au début du path
    path = f'/{language}{path}'

    # Reconstruire l'URL avec le path modifié (en excluant la partie domaine)
    redirect_url = urlunparse(parsed_url._replace(path=path))

    return redirect(redirect_url)  # Rediriger vers l'URL avec la langue appropriée

