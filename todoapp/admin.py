from django.contrib import admin

# Register your models here.
from todoapp.models import User, Tarea
from categorias.models import Categoria

admin.site.register(Categoria)
admin.site.register(Tarea)
admin.site.register(User)