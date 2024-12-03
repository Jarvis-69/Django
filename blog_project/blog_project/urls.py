# blog/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin
from blog import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.post_list, name='post_list'),
    path('create/', views.create_post, name='create_post'),
    path('modify/<int:pk>/', views.edit_post, name='edit_post'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('login/', auth_views.LoginView.as_view(next_page='post_list'), name='login'),
    path('logout/', views.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
