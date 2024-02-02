from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inicio/', views.inicio, name='inicio'),
    
    #Autenticación de usuarios del sistema.
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    #Perfil
    path('perfil/', views.perfil, name='perfil'),

    #Cambiar contraseña
    path('cambiar_contrasena_form/', views.cambiar_contrasena_form, name='cambiar_contrasena_form'),
    path('cambiar_clave/', views.cambiar_clave, name='cambiar_clave'),

    path('formulario_calc/', views.formulario_calc,name='formulario_calc'),

    path('calc/', views.calc, name='calc'),

    path('saludar/', views.saludar, name='saludar'),

    path('saludar_param/<str:nombre>/<str:apellido>', views.saludar_param, name='saludar_param'),

    path('calculadora/<int:num1>/<int:num2>/<str:operador>', views.calculadora, name='calculadora'), 

    #Carrito de compra
    path("carrito_add/", views.carrito_add, name="carrito_add"),
	path("carrito_ver/", views.carrito_ver, name="carrito_ver"),


    #CRUD DE CATEGORIAS

    path("categorias_listar/", views.categorias, name="categorias_listar"),
    path("categorias_form/", views.categorias_form, name="categorias_form"),
    path("categorias_crear/", views.categorias_crear, name="categorias_crear"),
    path("categorias_eliminar/<int:id>", views.categorias_eliminar, name="categorias_eliminar"),
    path("categorias_formulario_editar/<int:id>", views.categorias_formulario_editar, name="categorias_formulario_editar"),
    path("categorias_actualizar/", views.categorias_actualizar, name="categorias_actualizar"),
]                    