from django.contrib import admin

from .models import (
    Compra,
    Pedido,
    Factura
)

admin.site.register(Compra)
admin.site.register(Pedido)
admin.site.register(Factura)
