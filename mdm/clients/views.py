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


class ClienteRetrieveView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Cliente.objects.all()
    serializer_class = serializers.ClienteSerializer

    def list(self, request, *args, **kwargs):
        correo = self.request.GET.get('correo')
        try:
            cliente_id = ClienteInfo.objects.get(
                correo=correo,
                is_main=True
            ).cliente.id
            return Response(
                data={"Response": cliente_id},
                status=status.HTTP_302_FOUND
            )
        except Exception:
            return Response(
                data={"Response": "NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND
            )


class ClienteDeleteView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = Cliente.objects.all()
    serializer_class = serializers.ClienteSerializer

    def list(self, request, *args, **kwargs):
        correo = self.request.GET.get('correo')
        try:
            cliente_id = ClienteInfo.objects.get(
                correo=correo,
                is_main=True
            ).cliente.id
            Cliente.objects.filter(id=cliente_id).delete()
            return Response(
                data={"Response": "Success"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception:
            return Response(
                data={"Response": "Error"},
                status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request, *args, **kwargs):
        return Response(data="adding...")


class ClienteUpdateView(viewsets.GenericViewSet):
    queryset = Cliente.objects.all()
    serializer_class = serializers.ClienteSerializer

    def create(self, request, *args, **kwargs):
        correoActual = self.request.GET.get('correo')
        print(correoActual)
        try:
            cliente_id = ClienteInfo.objects.get(
                correo=correoActual,
                is_main=True
            ).cliente.id
            cliente = Cliente.objects.filter(id=cliente_id)
            serializer = serializers.CreateClienteSerializer(
                cliente,
                data=self.request.data.get('cliente'),
                partial=True
            )
            return Response(
                data={"Response": serializer.data},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception:
            return Response(
                data={"Response": "Error"},
                status=status.HTTP_404_NOT_FOUND
            )


class CarritoViewSet(viewsets.GenericViewSet):
    'List, create, retreive, update or delete carritos'
    queryset = Carrito.objects.all()
    serializer_class = serializers.CarritoSerializer

    def list(self, request, *args, **kwargs):
        return Response(
            data={"Error": "Unauthorized"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    def delete(self, cliente):
        Carrito.objects.filter(cliente_id=cliente.id).delete()

    def create(self, request, *args, **kwargs):
        correo = request.data.get('carrito')["correo"]
        cliente = ClienteInfo.objects.get(
            correo=correo,
            is_main=True
        ).cliente
        self.delete(cliente)
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


class CarritoRetrieveView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Carrito.objects.all()
    serializer_class = serializers.CarritoSerializer

    def list(self, request, *args, **kwargs):
        correo = self.request.GET.get('correo')
        try:
            cliente = ClienteInfo.objects.get(
                correo=correo,
                is_main=True
            ).cliente

            carrito = Carrito.objects.get(cliente=cliente)

            serializer = self.get_serializer(carrito)

            return Response(
                data=serializer.data,
                status=status.HTTP_302_FOUND
            )
        except Exception:
            return Response(
                data={"Response": "NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND
            )
