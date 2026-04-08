# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from todoapp.models import Tarea
from todoapp.models import User
from categorias.models import Categoria


def tareas(request):  # the index view
    
    if request.user.is_authenticated:
        mis_tareas = Tarea.objects.filter(owner=request.user)  # getting the tasks of the user with object manager and filter
    else:
        mis_tareas = Tarea.objects.filter(owner=None)  # if the user is not authenticated, show only the tasks without owner (public tasks)
        
    categorias = Categoria.objects.all()  # getting all categories with object manager

    if request.method == "GET":
        return render(request, "todoapp/index.html", {"tareas": mis_tareas, "categorias": categorias})
    if request.method == "POST":  # revisar si el método de la request es POST
        if "taskAdd" in request.POST:  # verificar si la request es para agregar una tarea (esto está definido en el button)
            titulo = request.POST["titulo"]  # titulo de la tarea
            nombre_categoria = request.POST["selector_categoria"]  # nombre de la categoria
            categoria = Categoria.objects.get(nombre=nombre_categoria)  # buscar la categoría en la base de datos
            contenido = request.POST["contenido"]  # contenido de la tarea

            #Verificar si el usuario inició sesión o no!!
            if request.user.is_authenticated:
                nueva_tarea = Tarea(titulo=titulo, contenido=contenido, categoria=categoria,owner=request.user)  # Crear la tarea
            else:
                nueva_tarea = Tarea(titulo=titulo, contenido=contenido, categoria=categoria)
            nueva_tarea.save()  # guardar la tarea en la base de datos.
            return redirect("/tareas")  # recargar la página.

def register_user(request):
    if request.method == "GET":
        return render(request, "todoapp/register_user.html")
    elif request.method == "POST":
        nombre = request.POST["nombre"]
        contraseña = request.POST["contraseña"]
        apodo = request.POST["apodo"]
        pronombre = request.POST["pronombre"]
        mail = request.POST["mail"]

        user = User.objects.create_user(username=nombre, password=contraseña, email=mail, apodo=apodo, pronombre=pronombre)

        return HttpResponseRedirect('/tareas')
    
def login_user(request):
    if request.method == 'GET':
        return render(request,"todoapp/login.html") 
    if request.method == 'POST':
        username = request.POST['username']
        contraseña = request.POST['contraseña']
        usuario = authenticate(username=username,password=contraseña)
        if usuario is not None:
            login(request,usuario)
            return HttpResponseRedirect('/tareas')
        else:
            return HttpResponseRedirect('/register')
        
 
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/tareas')
