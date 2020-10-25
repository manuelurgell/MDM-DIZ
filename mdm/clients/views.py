# views.py
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
)
# from rest_framework.viewsets import GenericViewSet

from .models import Carrito, CarritoInfo, Cliente
# from .serializers import CarritoSerializer, CarritoInfoSerializer
from rest_framework import status, viewsets
from rest_framework.response import Response


class SaveCarritoViewSet(viewsets.GenericViewSet,
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

        cliente = Cliente.objects.filter(email=email).values()
        cliente_id = cliente.id
        # insertar , crear el carrito
        carrito = Carrito.objects.create(
            cliente=cliente,
            fecha=datetime
        )
        carritoInfo = CarritoInfo.objects.create(
            carrito=carrito,
            codigoProductos=number,
            cantidadProductos=quantity
        )

        return Response(status=status.HTTP_200_OK, res='Todo bien')
