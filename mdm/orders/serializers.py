from rest_framework import serializers
from mdm.orders.models import Compra, Pedido, Factura


class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = [
            'cliente',
            'noTarjeta',
            'fecha',
            'total',
            'calle',
            'numero',
            'colonia',
            'ciudad',
            'cp',
            'estado',
            'entreCalles'
        ]


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = [
            'compra',
            'codigoProducto',
            'cantidadProducto',
            'precioProducto'
        ]


class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = [
            'compra',
            'RFC',
            'razonSocial',
            'fecha',
            'correo',
            'telefono',
            'calle',
            'numero',
            'colonia',
            'ciudad',
            'cp',
            'estado',
            'entreCalles'
        ]
