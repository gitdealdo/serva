from django.contrib import admin
from .models.detalle import Detalle
from .models.menu import Menu
from .models.tipo_menu import TipoMenu
from .models.insumos_detalle import InsumosDetalle


class DetalleAdmin(admin.ModelAdmin):
    '''
        Admin View for Detalle
    '''
    list_display = ('menu', 'receta', 'porcion', 'costo')
    search_fields = ('receta',)


class MenuAdmin(admin.ModelAdmin):
    '''
        Admin View for Menu
    '''
    list_display = ('tipo_menu', 'fecha')
    list_filter = ('fecha',)
    search_fields = ('fecha',)


admin.site.register(Menu, MenuAdmin)
admin.site.register(Detalle, DetalleAdmin)
admin.site.register(TipoMenu)
admin.site.register(InsumosDetalle)
