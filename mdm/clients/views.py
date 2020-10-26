# views.py
# from django import VERSION
# from django.db.models.fields import mixins
from mdm.clients.models import Carrito, Cliente, ClienteInfo
from mdm.clients import serializers

from rest_framework import status, viewsets
# from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
# from django.shortcuts import get_object_or_404


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
        serializer_cliente = serializers.ClienteSerializer(
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
                ).save()
            except Exception:
                Cliente.objects.filter(id=cliente.id).delete()
                return Response(status=status.HTTP_400_BAD_REQUEST)

            return Response(
                data={"response": "Success"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CarritoViewSet(viewsets.GenericViewSet):
    'List, create, retreive, update or delete carritos'
    queryset = Carrito.objects.all()
    serializer_class = serializers.CarritoSerializer


'''class SaveCarritoViewSet(viewsets.GenericViewSet,
                         CreateModelMixin,
                         RetrieveModelMixin,
                         UpdateModelMixin,
                         ListModelMixin):

    # serializer_class = CreateCarritoSerializer

    def create(self, request, *args, **kwargs):
        email = self.request.query_params.get('email', '0')
        datetime = self.request.query_params.get('datetime', '0')
        number = self.request.query_params.get('number', '0')
        quantity = self.request.query_params.get('quantity', '0')

        cliente = ClienteInfo.objects.filter(correo=email).values()
        # cliente_id = cliente.id
        # insertar, crear el carrito
        carrito = Carrito.objects.create(
            cliente=cliente,
            fecha=datetime
        )
        CarritoInfo.objects.create(
            carrito=carrito,
            codigoProductos=number,
            cantidadProductos=quantity
        )

        # return Response(status=status.HTTP_200_OK, res='Todo bien')
        return HttpResponse("Todo bien")'''
