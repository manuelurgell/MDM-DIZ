from django.contrib import admin

from mdm.clients.models import (
    Carrito,
    CarritoInfo,
    Cliente,
    ClienteInfo,
    CodigoPostal,
    NameException
)


class NameExceptionAdmin(admin.ModelAdmin):
    model = NameException
    list_display = (
        'id',
        'nombre'
    )


class CodigoPostalAdmin(admin.ModelAdmin):
    model = CodigoPostal
    list_display = (
        'id',
        'codigo'
    )


class ClienteAdmin(admin.ModelAdmin):
    model = Cliente
    list_display = (
        'id',
        'nombrePila',
        'apellidoPat',
        'created_date',
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
        'fecha'
    )


class CarritoInfoAdmin(admin.ModelAdmin):
    model = CarritoInfo
    list_display = (
        'carrito_id',
        'codigoProducto',
        'cantidadProducto'
    )


# Register tour models here
admin.site.register(NameException, NameExceptionAdmin)
admin.site.register(CodigoPostal, CodigoPostalAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(ClienteInfo, ClienteInfoAdmin)
admin.site.register(Carrito, CarritoAdmin)
admin.site.register(CarritoInfo, CarritoInfoAdmin)
