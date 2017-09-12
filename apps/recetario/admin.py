from django.contrib import admin

from .models.categoria import Categoria
from .models.unidad import Unidad
from .models.producto import Producto
from .models.ingrediente import Ingrediente
from .models.tipo_receta import TipoReceta
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
    list_display = ('nombre', 'tipo_receta', 'porcion')
    list_filter = ('nombre', 'tipo_receta',)
    search_fields = ('nombre',)


admin.site.register(Categoria)
admin.site.register(Unidad)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Ingrediente, IngredienteAdmin)
admin.site.register(TipoReceta)
admin.site.register(Receta, RecetaAdmin)
