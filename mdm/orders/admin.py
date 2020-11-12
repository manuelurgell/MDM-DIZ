from django.contrib import admin

from .models import (
    Compra,
    Factura,
    Pedido
)


class CompraAdmin(admin.ModelAdmin):
    model = Compra
    list_display = (
        'cliente_id',
        'id',
        'fecha',
        'total'
    )


class PedidoAdmin(admin.ModelAdmin):
    model = Pedido
    list_display = (
        'compra_id',
        'id',
        'codigoProducto',
        'cantidadProducto',
        'precioProducto'
    )


class FacturaAdmin(admin.ModelAdmin):
    model = Pedido
    list_display = (
        'compra_id',
        'id',
        'RFC',
        'fecha'
    )


admin.site.register(Compra, CompraAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Factura)
