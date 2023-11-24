from django.shortcuts import render, redirect
from django.contrib import messages

def login_requerido(vista):
    def nueva_funcion(request):
        logueo = request.session.get("logueo", False)
        #Autencticación y autorización
        if logueo and logueo["rol"] == 1:
            c = vista(request)
            return c
        else:
            messages.info(request, "No está autorizado.")
            return redirect("index")
    return nueva_funcion