from mdm.orders.models import Compra, Pedido, Factura
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
        dataCompra = request.data.get('compra')
        correo = dataCompra["correo"]
        cliente = ClienteInfo.objects.get(
            correo=correo,
            is_main=True
        ).cliente
        try:
            compra = Compra.objects.create(
                cliente=cliente,
                noTarjeta=dataCompra["noTarjeta"],
                total=dataCompra["total"],
                calle=dataCompra["calle"],
                numero=dataCompra["numero"],
                colonia=dataCompra["colonia"],
                ciudad=dataCompra["ciudad"],
                cp=dataCompra["cp"],
                estado=dataCompra["estado"],
                entreCalles=dataCompra["entreCalles"]
            )
            try:
                dataPedido = request.data.get('pedido')

                Pedido.objects.create(
                    compra=compra,
                    codigoProducto=dataPedido["codigoProducto"],
                    cantidadProducto=dataPedido["cantidadProducto"],
                    precioProducto=dataPedido["precioProducto"]
                ).save()
            except Exception:
                Compra.objects.filter(id=compra.id).delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(compra)

        return Response(
            # data={"response": "Success"},
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


class FacturaViewSet(viewsets.ModelViewSet):
    '''List, create, retrieve, update, partial_update or delete compras'''
    queryset = Factura.objects.all()
    serializer_class = serializers.FacturaSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        compra_id = data["compra_id"]
        compra = Compra.objects.get(
            id=compra_id
        )
        factura = Factura.objects.create(
            compra=compra,
            RFC=data["RFC"],
            razonSocial=data["razonSocial"],
            correo=data["correo"],
            telefono=data["telefono"],
            calle=data["calle"],
            numero=data["numero"],
            colonia=data["colonia"],
            ciudad=data["ciudad"],
            cp=data["cp"],
            estado=data["estado"],
            entreCalles=data["entreCalles"]
        )
        try:
            serializer = self.get_serializer(factura)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(
            # data={"response": "Success"},
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )
