
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('pacientes/', include('apps.pacientes.urls')),
    path('valoracion/', include('apps.valoracion.urls')),
    path('seguimiento/', include('apps.seguimiento.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    
]
handler404 = 'core.views.error_404'