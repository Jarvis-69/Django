# blog/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib import admin
from blog import views
from django.contrib.auth import views as auth_views
from rosetta import urls as rosetta_urls
from django.urls import include
from django.conf.urls.i18n import i18n_patterns
from blog.views import set_language

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rosetta/', include(rosetta_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('set_language/', set_language, name='set_language'),
    path('', views.post_list, name='post_list'),
    path('create/', views.create_post, name='create_post'),
    path('modify/<int:pk>/', views.edit_post, name='edit_post'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('login/', auth_views.LoginView.as_view(next_page='post_list'), name='login'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('logout/', views.logout_view, name='logout'),
)
