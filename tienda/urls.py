from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_productos, name="lista_productos"),
    path("agregar/<int:producto_id>/", views.agregar_carrito, name="agregar_carrito"),
    path("carrito/", views.ver_carrito, name="ver_carrito"),
    path('finalizar/', views.finalizar_compra, name='finalizar_compra'),
]