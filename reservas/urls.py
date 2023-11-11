from django.urls import path
from . import views
from .views import generate_pdf

urlpatterns = [

    path('', views.index, name='index'),
    path('fazer_reserva/', views.fazer_reserva, name='fazer_reserva'),
    path('gerar_pdf/', generate_pdf, name='generate_pdf'),
]