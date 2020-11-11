from mdm.clients.models import Carrito, CarritoInfo, Cliente, ClienteInfo, Exceptions
from mdm.clients import serializers

from rest_framework import status, viewsets, mixins
# from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_number

import re

# Create your views here


class ClientViewSet(viewsets.ModelViewSet):
    '''List, create, retrieve, update, partial_update or delete clientes'''
    queryset = Cliente.objects.all()
    serializer_class = serializers.ClienteSerializer

    def ValidateName(self, clientName):
        try:
            Exceptions.objects.get(nombre=clientName)
            return True
        except Exceptions.DoesNotExist:
            return bool(
                re.match(
                    '^[^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$', clientName)
                        )

    def ValidateEmail(self, email):
        # print(email)
        try:
            validate_email(email)
            valid_email = True
        except ValidationError:
            valid_email = False
        return valid_email

    def ValidatePhone(self, phone):
        try:
            if len(phone) == 10:
                cel = phonenumbers.parse(phone, "MX")
            else:
                phone = '+'+phone
                parse = phonenumbers.parse(phone)
                region = region_code_for_number(parse)
                cel = phonenumbers.parse(phone, region)
            print(cel)
            valid_phone = phonenumbers.is_possible_number(cel)
            valid_phone = phonenumbers.is_valid_number(cel)
        except Exception:
            valid_phone = False
        return valid_phone

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
            clientName = dataCliente["nombrePila"]
            validName = self.ValidateName(clientName)
            phone = dataClienteInfo["telefono"]
            check = self.ValidatePhone(phone)
            email = dataClienteInfo["correo"]
            check2 = self.ValidateEmail(email)
            if check and check2 and validName:
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
                Cliente.objects.filter(id=cliente.id).delete()
                if not validName:
                    return Response(
                        data={
                            "Response": "NOT A CORRECT NAME"
                        },
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
                if not check and not check2:
                    return Response(
                        data={
                            "Response": "NOT A CORRECT PHONE AND NOT AN EMAIL"
                        },
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
                if not check:
                    return Response(
                        data={"Response": "NOT A CORRECT PHONE"},
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
                else:
                    return Response(
                        data={"Response": "NOT AN EMAIL"},
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            cliente = self.get_object()
            if not cliente.is_deleted:
                serializer = self.get_serializer(cliente)
                data = serializer.data
            else:
                return Response(
                    data={"Response": "NOT_FOUND"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception:
            return Response(
                data={"Response": "NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            data=data,
            status=status.HTTP_302_FOUND
        )

    def destroy(self, request, *args, **kwargs):
        # self.perform_destroy(cliente)
        try:
            cliente = self.get_object()
            if not cliente.is_deleted:
                cliente.is_deleted = True
                cliente.save()
                serializer = self.get_serializer(cliente)
                data = serializer.data
            else:
                return Response(
                    data={"Response": "NOT_FOUND"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception:
            return Response(
                data={"Response": "NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            data=data,
            status=status.HTTP_301_MOVED_PERMANENTLY
        )


class ClienteRetrieveView(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Cliente.objects.all()
    serializer_class = serializers.ClienteSerializer

    def list(self, request, *args, **kwargs):
        correo = self.request.GET.get('correo')
        try:
            clientesInfo = ClienteInfo.objects.filter(
                correo=correo,
                is_main=True
            )
            cliente = Cliente.objects
            for clienteInfo in clientesInfo:
                cliente = clienteInfo.cliente
                if not cliente.is_deleted:
                    return Response(
                        data={"Response": cliente.id},
                        status=status.HTTP_302_FOUND
                    )
            return Response(
                data={"Response": "NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            return Response(
                data={"Response": "NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND
            )


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
