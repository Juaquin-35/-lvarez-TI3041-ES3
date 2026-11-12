from django.contrib import admin
from .models import Categoria, Producto, ConsultaCliente


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # list_display muestra 4 campos (cumple con el mínimo de 3)
    list_display = ('nombre', 'categoria', 'precio', 'stock')
    # Búsqueda por nombre de producto y por el nombre de la categoría asociada
    search_fields = ('nombre', 'categoria__nombre')
    # Filtro lateral por categoría
    list_filter = ('categoria',)

@admin.register(ConsultaCliente)
class ConsultaClienteAdmin(admin.ModelAdmin):
    # Campos que se verán en el listado del panel de administración
    list_display = ('nombre', 'correo', 'producto_interes', 'fecha')
    # Campos por los que se podrá buscar en el panel de administración
    search_fields = ('nombre', 'correo', 'mensaje')
    # Filtro lateral por fecha de creación o producto de interés
    list_filter = ('fecha', 'producto_interes')
    # Hacer que la fecha sea de solo lectura por seguridad/historial
    readonly_fields = ('fecha',)