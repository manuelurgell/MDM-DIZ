from django.contrib import admin

from mdm.clients.models import (
    Exceptions,
    Cliente,
    ClienteInfo,
    Carrito,
    CarritoInfo,
)


class ExceptionsAdmin(admin.ModelAdmin):
    model = Exceptions
    list_display = (
        'id',
        'nombre'
    )


class ClienteAdmin(admin.ModelAdmin):
    model = Cliente
    list_display = (
        'id',
        'nombrePila',
        'apellidoPat',
        'created',
        'is_deleted'
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


class CarritoAdmin(admin.ModelAdmin):
    model = Carrito
    list_display = (
        'cliente_id',
        'id',
        'fecha'
    )


class CarritoInfoAdmin(admin.ModelAdmin):
    model = CarritoInfo
    list_display = (
        'carrito_id',
        'id',
        'codigoProducto',
        'cantidadProducto'
    )


# Register tour models here
admin.site.register(Exceptions, ExceptionsAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(ClienteInfo, ClienteInfoAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(CarritoInfo, CarritoInfoAdmin)
