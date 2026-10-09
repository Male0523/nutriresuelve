from django.urls import path
from . import views

urlpatterns = [
    path('valorar/<int:paciente_id>/', views.valorar_paciente, name='valorar_paciente'),
    path('recomendacion/<int:recomendacion_id>/', views.ver_recomendacion, name='ver_recomendacion'),
]