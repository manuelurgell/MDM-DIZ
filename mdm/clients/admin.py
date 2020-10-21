from django.contrib import admin

from .models import (
    Cliente,
    ClienteInfo,
    Carrito,
    CarritoInfo
)

admin.site.register(Cliente)
admin.site.register(ClienteInfo)
admin.site.register(Carrito)
admin.site.register(CarritoInfo)
