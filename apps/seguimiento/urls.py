from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_seguimientos, name='lista_seguimientos'),
    path('<int:paciente_id>/', views.seguimiento_paciente, name='seguimiento_paciente'),
]