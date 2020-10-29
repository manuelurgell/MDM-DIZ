from mdm.clients.models import Carrito, CarritoInfo, Cliente, ClienteInfo
from mdm.clients import serializers

from rest_framework import status, viewsets, mixins
# from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

# Create your views here


class ClientViewSet(viewsets.ModelViewSet):
    '''List, create, retrieve, update, partial_update or delete clientes'''
    queryset = Cliente.objects.all()
    serializer_class = serializers.ClienteSerializer

    def list(self, request, *args, **kwargs):
        return Response(
            data={"Error": "Unauthorized"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    def create(self, request, *args, **kwargs):
        dataCliente = request.data.get('cliente')
        serializer_cliente = serializers.CreateClienteSerializer(
            data=dataCliente
        )
        if serializer_cliente.is_valid():
            cliente = serializer_cliente.save()
            dataClienteInfo = request.data.get('clienteInfo')

            try:
                ClienteInfo.objects.create(
                    cliente=cliente,
                    telefono=dataClienteInfo["telefono"],
                    correo=dataClienteInfo["correo"],
                    is_main=True
                )
            except Exception:
                Cliente.objects.filter(id=cliente.id).delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(
                cliente
            )

            return Response(
                # data={"response": "Success"},
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        return Response(pk)


class ClienteRetrieveView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Cliente.objects.all()
    serializer_class = serializers.ClienteSerializer

    def list(self, request, *args, **kwargs):
        email = self.request.GET.get('email')
        return Response(email)


class CarritoViewSet(viewsets.GenericViewSet):
    'List, create, retreive, update or delete carritos'
    queryset = Carrito.objects.all()
    serializer_class = serializers.CarritoSerializer

    def list(self, request, *args, **kwargs):
        return Response(
            data={"Error": "Unauthorized"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    def create(self, request, *args, **kwargs):
        correo = request.data.get('carrito')["correo"]
        cliente = ClienteInfo.objects.get(
            correo=correo,
            is_main=True
        ).cliente

        try:
            carrito = Carrito.objects.create(
                cliente=cliente
            )
            try:
                dataCarritoInfo = request.data.get('carritoInfo')
                CarritoInfo.objects.create(
                    carrito=carrito,
                    codigoProducto=dataCarritoInfo["codigoProducto"],
                    cantidadProducto=dataCarritoInfo["cantidadProducto"]
                )

                serializer = serializers.CarritoSerializer(
                    carrito
                )

                return Response(
                    # data={"response": "Success"},
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                )
            except Exception:
                Carrito.objects.filter(id=carrito.id).delete()
                return Response(data="1", status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
