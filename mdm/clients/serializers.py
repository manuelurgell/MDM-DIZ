# serializers.py
from rest_framework import serializers
from mdm.clients.models import Cliente, Carrito, CarritoInfo, ClienteInfo


class ClienteSerializer(serializers.ModelSerializer):
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
            'cuidad',
            'cp',
            'estado',
            'entreCalles',
            'is_main'
        ]


class CarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito
        fields = [
            'cliente',
            'fecha'
        ]


class CarritoInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarritoInfo
        fields = [
            'carrito',
            'codigoProductos',
            'cantidadProductos'
        ]
