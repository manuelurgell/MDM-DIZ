from rest_framework import serializers

from mdm.clients.models import Cliente
from mdm.orders.models import Compra, Factura, Pedido


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = [
            'codigoProducto',
            'cantidadProducto',
            'precioProducto'
        ]


class CompraSerializer(serializers.ModelSerializer):
    pedido = PedidoSerializer(many=True)

    class Meta:
        model = Compra
        fields = [
            'id',
            'noTarjeta',
            'mesTarjeta',
            'anioTarjeta',
            'fecha',
            'total',
            'calle',
            'numero',
            'colonia',
            'ciudad',
            'cp',
            'estado',
            'entreCalles',
            'pedido'
        ]


class FacturaSerializer(serializers.ModelSerializer):
    compra = CompraSerializer(many=True)

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
            'entreCalles',
            'compra'
        ]


class ClienteSerializer(serializers.ModelSerializer):
    compra = CompraSerializer(many=True)

    class Meta:
        model = Cliente
        fields = [
            'id',
            'compra'
        ]
