from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

#Importamos todos los modelos 
from .models import *

#Importamos el archivo de decoradoes
from .decorador_especial import *

# Create your views here.

def index(request):
    logueo = request.session.get("logueo", False)
    if logueo == False:
        return render(request, "tienda/login/login.html")
    else:
        return redirect("inicio")


def login(request):
    if request.method == "POST":
        user = request.POST.get("correo")
        passw= request.POST.get("clave")
        #select * from Usuario where correo = "user" and clave = "passw"
        try:
            q = Usuario.objects.get(correo = user, clave = passw)
            #Crear Variable de sesión
            request.session["logueo"] = {
                "id": q.id,
                "nombre": q.nombre,
                "rol": q.rol
            }
            messages.success(request, f"Bienvenido {q.nombre}!!")
            return redirect ("inicio")
        except Exception as e:
            messages.error(request, f"Error: Usuario o contraseña incorrectos...")
            return redirect ("index")
    else:
        messages.warning(request, 'Error: No se enviaron datos...')
        return redirect("index")
    
def logout (request):
    try:
        del request.session["logueo"]
        messages.success(request, "Sesión cerrada correctamente!")
        return redirect("index")
    except Exception as e:
        messages.warning(request, "No se pudo cerrar sesión...")
        return redirect("inicio")

def inicio(request):
    logueo = request.session.get("logueo", False)
    if logueo:
        return render(request, "tienda/inicio.html")
    else:
        return redirect("index")

def saludar(request):
    return HttpResponse("Hola, <strong style='color:red'>A todos!!</strong>")

def saludar_param(request, nombre, apellido):
    return HttpResponse(f"Hola, <strong style='color:red'>{nombre} {apellido}</strong>")


#Construir una miniCalculadora, que haga operaciones con dos números

def calculadora(request, num1, num2, operador):
    if operador == "suma":
        return HttpResponse(f"La suma de {num1} + {num2} es: <strong style='color:red'>{num1 + num2}</strong>")
    elif operador == "resta":
        return HttpResponse(f"La resta de {num1} - {num2} es: <strong style='color:red'>{num1 - num2}</strong>")
    elif operador == "multiplicacion":
        return HttpResponse(f"La multiplicación de {num1} * {num2} es: <strong style='color:red'>{num1 * num2}</strong>")
    elif operador == "division":
        return HttpResponse(f"La division de {num1} / {num2} es: <strong style='color:red'>{num1 / num2}</strong>")
    else:
        return HttpResponse("Operador no valido")
    


def formulario_calc(request):
    return render(request, "tienda/formulario_calc.html")

def calc(request):
    num1 = int(request.POST.get("num1"))
    num2 = int(request.POST.get("num2"))
    oper = request.POST.get("oper")
    if oper == "1":
        return HttpResponse(f"La suma de {num1} + {num2} es: <strong style='color:red'>{num1 + num2}</strong>")
    elif oper == "2":
        return HttpResponse(f"La resta de {num1} - {num2} es: <strong style='color:red'>{num1 - num2}</strong>")
    elif oper == "3":
        return HttpResponse(f"La multiplicación de {num1} * {num2} es: <strong style='color:red'>{num1 * num2}</strong>")
    elif oper == "4":
        return HttpResponse(f"La division de {num1} / {num2} es: <strong style='color:red'>{num1 / num2}</strong>")
    else:
        return HttpResponse("Operador no valido")
    
@login_requerido
def categorias(request):
    #select * from categorias
    logueo = request.session.get("logueo", False)
    #Autencticación y autorización
    if logueo and logueo["rol"] == 1:
        q = Categoria.objects.all()
        print(q)
        contexto = {"data": q}
        return render(request,"tienda/categorias/categorias.html", contexto)
    else:
        messages.info(request, "No está autorizado.")
        return redirect("index")


def categorias_form(request):
    return render(request, 'tienda/categorias/categorias_form.html')

def categorias_crear(request):
    if request.method == "POST":
        nomb = request.POST.get("nombre")
        desc = request.POST.get("descripcion")
        try:
        # INSERT INTO Categoria (nombre, descripcion) VALUES (nomb, desc)
            ob1 = Categoria(
                nombre = nomb, 
                descripcion = desc
                )
            ob1.save()
            messages.success(request, 'Guardado Correctamente!!')
        except Exception as e:
            messages.error(request, f'Error: {e}')
        return redirect('categorias_listar')
        
    else:
        messages.warning (request, f'Error: No se enviaron datos...')
        return redirect('categorias_listar')

def categorias_eliminar(request, id):
    try:
        ob1 = Categoria.objects.get(pk = id)
        ob1.delete()
        messages.success(request, "Categoría eliminada correctamente")
    except Exception as e:
        messages.error(request, f"Error: {e}")

    return redirect("categorias_listar")


def categorias_formulario_editar(request, id):
    ob1 = Categoria.objects.get(pk = id)
    contexto = {"data": ob1}
    return render(request, "tienda/categorias/categorias_formulario_editar.html", contexto)

def categorias_actualizar(request):
    if request.method == "POST":
        id = request.POST.get("id") 
        nomb = request.POST.get("nombre")
        desc = request.POST.get("descripcion")
        try:
            ob1 = Categoria.objects.get(pk=id)
            ob1.nombre = nomb
            ob1.descripcion = desc
            ob1.save()
            messages.success(request, "Categoría actualizada correctamente")
        except Exception as e:
            messages.error(request, f"Error: {e}")
    else:
        messages.warning (request, f'Error: No se enviaron datos...')
        
    return redirect('categorias_listar')

