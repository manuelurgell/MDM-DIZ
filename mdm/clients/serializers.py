# serializers.py
from rest_framework import serializers

from mdm.clients.models import Carrito, CarritoInfo, Cliente, ClienteInfo
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
            'cliente',
            'telefono',
            'correo',
            'calle',
            'colonia',
            'ciudad',
            'cp',
            'estado',
            'entreCalles',
            'is_main'
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
            'carrito',
            'codigoProducto',
            'cantidadProducto'
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


class CreateCarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'cliente',
            'fecha'
        ]
