from django.contrib import admin

from mdm.clients.models import (
    Cliente,
    ClienteInfo,
    Carrito,
    CarritoInfo
)


class ClienteAdmin(admin.ModelAdmin):
    model = Cliente
    list_display = (
        'id',
        'nombrePila',
        'apellidoPat',
        'created'
    )


class ClienteInfoAdmin(admin.ModelAdmin):
    model = Cliente
    list_display = (
        'cliente_id',
        'id',
        'telefono',
        'correo',
        'is_main'
    )


# Register tour models here
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(ClienteInfo, ClienteInfoAdmin)
admin.site.register(Carrito)
admin.site.register(CarritoInfo)
