from django.contrib import admin
from .models import Perfil, Gasto, Categoria

# Register your models here.
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'email', 'user',  'limite')

@admin.register(Gasto)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'descricao')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('categoria_nome', 'limite_categoria', 'user')