from django.contrib import admin

from .models.tipo import Tipo
from .models.unidad import Unidad
from .models.producto import Producto
from .models.ingrediente import Ingrediente
from .models.categoria import Categoria
from .models.receta import Receta


class ProductoAdmin(admin.ModelAdmin):
    '''
        Admin View for Producto
    '''
    list_display = ('nombre', 'categoria', 'unidad',)
    list_filter = ('nombre',)
    search_fields = ('nombre',)


class IngredienteAdmin(admin.ModelAdmin):
    '''
        Admin View for Ingrediente
    '''
    list_display = ('producto', 'cantidad', 'receta')
    list_filter = ('producto',)
    search_fields = ('receta',)


class RecetaAdmin(admin.ModelAdmin):
    '''
        Admin View for Receta
    '''
    list_display = ('nombre', 'categoria', 'porcion', 'costo', 'user')
    list_filter = ('nombre', 'user', 'categoria',)
    search_fields = ('nombre',)


admin.site.register(Tipo)
admin.site.register(Unidad)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Ingrediente, IngredienteAdmin)
admin.site.register(Categoria)
admin.site.register(Receta, RecetaAdmin)
