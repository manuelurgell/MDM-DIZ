from mdm.orders.models import Compra, Pedido
from mdm.clients.models import ClienteInfo
from mdm.orders import serializers

from rest_framework import status, viewsets
from rest_framework.response import Response


# Create your views here.
class CompraViewSet(viewsets.ModelViewSet):
    '''List, create, retrieve, update, partial_update or delete compras'''
    queryset = Compra.objects.all()
    serializer_class = serializers.CompraSerializer

    def create(self, request, *args, **kwargs):
        dataCompraR = request.data.get('compra')
        correoCompra = dataCompraR["correo"]
        cliente = ClienteInfo.objects.get(
            correo=correoCompra,
            is_main=True
        ).cliente
        try:
            compra = Compra.objects.create(
                cliente=cliente,
                noTarjeta=dataCompraR["noTarjeta"],
                fecha=dataCompraR["fecha"],
                total=dataCompraR["total"],
                calle=dataCompraR["calle"],
                numero=dataCompraR["numero"],
                colonia=dataCompraR["colonia"],
                ciudad=dataCompraR["ciudad"],
                cp=dataCompraR["cp"],
                estado=dataCompraR["estado"],
                entreCalles=dataCompraR["entreCalles"]
            ).save()
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        dataPedido = request.data.get('pedido')

        Pedido.objects.create(
            compra_id=compra.id,
            codigoProducto=dataPedido["codigoProducto"],
            cantidadProducto=dataPedido["cantidadProducto"],
            precioProducto=dataPedido["precioProducto"]
        ).save()

        return Response(
            data={"response": "Success"},
            status=status.HTTP_201_CREATED
        )
