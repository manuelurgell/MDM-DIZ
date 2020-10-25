# serializers.py
from rest_framework import serializers

from .models import Carrito,  CarritoInfo


class CarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito
        fields = (
            'id', 'cliente', 'fecha'
        )


class CarritoInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarritoInfo
        fields = (
            'id', 'carrito', 'codigoProductos', 'cantidadProductos'
        )


class CreateCarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito
        fields = (
            'id', 'cliente', 'fecha'
        )


class CreateCarritoInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarritoInfo
        fields = (
            'id', 'carrito', 'codigoProductos', 'cantidadProductos'
        )
