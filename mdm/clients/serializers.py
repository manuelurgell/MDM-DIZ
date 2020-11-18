# serializers.py
from rest_framework import serializers

from mdm.clients.models import (
    Carrito,
    CarritoInfo,
    Cliente,
    ClienteInfo,
    CodigoPostal
)
from mdm.orders.serializers import CompraSerializer


class CreateClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'nombrePila',
            'apellidoPat',
            'apellidoMat',
            'fechaNac',
            'genero'
        ]


class ClienteInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClienteInfo
        fields = [
            'telefono',
            'correo',
            'noTarjeta',
            'mesTarjeta',
            'anioTarjeta',
            'calle',
            'colonia',
            'ciudad',
            'cp',
            'estado',
            'entreCalles',
            'is_main'
        ]


class UpdateClienteSerializer(serializers.ModelSerializer):
    clienteInfo = ClienteInfoSerializer(many=True)

    class Meta:
        model = Cliente
        fields = [
            'nombrePila',
            'apellidoPat',
            'apellidoMat',
            'fechaNac',
            'genero',
            'clienteInfo'
        ]


class ClienteSerializer(serializers.ModelSerializer):
    clienteInfo = ClienteInfoSerializer(many=True)
    compra = CompraSerializer(many=True)

    class Meta:
        model = Cliente
        fields = [
            'id',
            'nombrePila',
            'apellidoPat',
            'apellidoMat',
            'fechaNac',
            'genero',
            'is_deleted',
            'clienteInfo',
            'compra'
        ]


class CarritoInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarritoInfo
        fields = [
            'codigoProducto',
            'cantidadProducto'
        ]


class CreateCarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'cliente',
            'fecha'
        ]


class CarritoSerializer(serializers.ModelSerializer):
    carritoInfo = CarritoInfoSerializer(many=True)

    class Meta:
        model = Carrito
        fields = [
            'cliente',
            'fecha',
            'carritoInfo'
        ]


class CodigoPostalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodigoPostal
        fields = [
            'codigo',
            'colonia',
            'municipio',
            'estado'
        ]
