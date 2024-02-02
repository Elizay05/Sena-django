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
                "rol": q.rol,
                "nombre_rol": q.get_rol_display()
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
        del request.session["carrito"]
        messages.success(request, "Sesión cerrada correctamente!")
        return redirect("index")
    except Exception as e:
        messages.warning(request, "No se pudo cerrar sesión...")
        return redirect("inicio")

def inicio(request):
    logueo = request.session.get("logueo", False)
    if logueo:
        categorias = Categoria.objects.all()
        
        cat = request.GET.get("cat")
        if cat == None:
            productos = Productos.objects.all()
        else:
            c = Categoria.objects.get(pk=cat)
            productos = Productos.objects.filter(categoria=c)
        contexto = {"data": productos, "cat":categorias}
        return render(request, "tienda/inicio.html", contexto)
    else:
        return redirect("index")


def perfil(request):
    logueo = request.session.get("logueo", False)
    # Consultamos en DB por el ID del usuario logueado...
    q = Usuario.objects.get(pk=logueo["id"])
    contexto = {"data": q}
    return render(request, "tienda/login/perfil.html", contexto)

def cambiar_contrasena_form(request):
    return render(request, "tienda/login/cambio_contrasena.html")

def cambiar_clave(request):
    if request.method == "POST":
        logueo = request.session.get("logueo", False)
        q = Usuario.objects.get(pk=logueo["id"])
        c1 = request.POST.get("nueva1")
        c2 = request.POST.get("nueva2")
        if q.clave == request.POST.get("clave"):
            if c1 == c2:
                #Cambiar clave en DB
                q.clave = c1
                q.save()
                messages.success(request, "Contraseña guardada correctamente!")
            else:
                messages.info(request, "Las contraseñas nuevas no coinciden...")
        else:
            messages.error(request, "Contraseña no válida...")
    else:
        messages.warning(request, "Error: No se enviaron datos...")
    
    return redirect('cambiar_contrasena_form')


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


def carrito_add(request):
	if request.method == "POST":
		try:
			carrito = request.session.get("carrito", False)
			if not carrito:
				request.session["carrito"] = []
				carrito = []

			id_producto = int(request.POST.get("id"))
			cantidad = request.POST.get("cantidad")
			# Consulto el producto en DB...........................
			q = Productos.objects.get(pk=id_producto)
			for p in carrito:
				if p["id"] == id_producto:
					if q.inventario >= (p["cantidad"] + int(cantidad)) and int(cantidad) > 0:
						p["cantidad"] += int(cantidad)
						p["subtotal"] = p["cantidad"] * q.precio
					else:
						print("Cantidad supera inventario...")
						messages.warning(request, "Cantidad supera inventario...")
					break
			else:
				print("No existe en carrito... lo agregamos")
				if q.inventario >= int(cantidad) and int(cantidad) > 0:
					carrito.append(
						{
							"id": q.id,
							"foto": q.foto.url,
							"producto": q.nombre,
							"cantidad": int(cantidad),
							"subtotal": int(cantidad) * q.precio
						}
					)
				else:
					print("Cantidad supera inventario...")
					messages.warning(request, "No se puede agregar, no hay suficiente inventario.")

			# Actualizamos variable de sesión carrito...
			request.session["carrito"] = carrito

			contexto = {
				"items": len(carrito),
				"total": sum(p["subtotal"] for p in carrito)
			}
			return render(request, "tienda/carrito/carrito.html", contexto)
		except ValueError as e:
			messages.error(request, f"Error: Digite un valor correcto para cantidad")
			return HttpResponse("Error")
		except Exception as e:
			messages.error(request, f"Ocurrió un Error: {e}")
			return HttpResponse("Error")
	else:
		messages.warning(request, "No se enviaron datos.")
		return HttpResponse("Error")



def carrito_ver(request):
	carrito = request.session.get("carrito", False)
	if not carrito:
		request.session["carrito"] = []
		contexto = {
			"items": 0,
			"total": 0
		}
	else:
		contexto = {
			"items": len(carrito),
			"total": sum(p["subtotal"] for p in carrito)
		}
	return render(request, "tienda/carrito/carrito.html", contexto)

