import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_number

from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from mdm.clients import serializers
from mdm.clients.models import (
    Carrito,
    CarritoInfo,
    Cliente,
    ClienteInfo,
    CodigoPostal,
    NameException
)
from mdm.utils import call_me

# Create your views here


class ClientViewSet(viewsets.ModelViewSet):
    '''List, create, retrieve, update, partial_update or destroy clientes'''
    queryset = Cliente.objects.all()
    serializer_class = serializers.ClienteSerializer

    def validateGender(self, clientName, gender):
        try:
            if gender == "H" or gender == "M" or gender == "O":
                if re.match('.*[Aa]$', clientName) and gender == "H":
                    valido = False
                elif re.match('.*(OS|o|O|os)$', clientName) and gender == "M":
                    valido = False
                else:
                    valido = True
            else:
                valido = False
        except Exception:
            valido = False
        return valido

    def ValidateName(self, clientName):
        try:
            NameException.objects.get(nombre=clientName)
            valido = True
        except NameException.DoesNotExist:
            valido = bool(
                re.match(
                    r'^[^0-9_!¡?÷?¿/\\+=@#$%ˆ&*(){}|~<>;:[\]]{2,}$',
                    clientName
                )
            )
        return valido

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

    def Duplicate(self, email):
        try:
            cliente = ClienteInfo.objects.get(correo=email).cliente
            Cliente.objects.get(id=cliente.id, is_deleted=False)
            duplicate = False
        except ClienteInfo.DoesNotExist:
            duplicate = True
        except Cliente.DoesNotExist:
            duplicate = True
        return duplicate

    def CheckDuplicate(self, clientName, clientLast, birth, gender, phone):
        try:
            temporaryClient = Cliente.objects.get(
                nombrePila=clientName,
                apellidoPat=clientLast,
                fechaNac=birth,
                genero=gender,
                is_deleted=False
            )
            temporaryId = temporaryClient.id
        except Cliente.DoesNotExist:
            temporaryId = "0"
        return temporaryId

    def create(self, request, *args, **kwargs):
        dataCliente = request.data.get('cliente')
        serializer_cliente = serializers.CreateClienteSerializer(
            data=dataCliente
        )
        if serializer_cliente.is_valid():
            dataClienteInfo = request.data.get('clienteInfo')
            clientName = dataCliente["nombrePila"]
            clientLast = dataCliente["apellidoPat"]
            validName = self.ValidateName(clientName)
            phone = dataClienteInfo["telefono"]
            birth = dataCliente["fechaNac"]
            gender = dataCliente["genero"]
            checkGender = self.validateGender(clientName, gender)
            check = self.ValidatePhone(phone)
            email = dataClienteInfo["correo"]
            check2 = self.ValidateEmail(email)
            check1 = self.Duplicate(email)
            if check and check1 and check2 and validName and checkGender:
                duplicateName = self.CheckDuplicate(
                    clientName, clientLast, birth, gender, phone
                )
                if duplicateName != "0":
                    existingClientInfo = ClienteInfo.objects.get(
                        cliente=duplicateName,
                        is_main=True
                    )
                    if phone == existingClientInfo.telefono:
                        ClienteInfo.objects.filter(
                            cliente=duplicateName
                        ).update(is_main=False)
                        notTheSame = False

                        clienteInfo = ClienteInfo.objects.create(
                            cliente=existingClientInfo.cliente,
                            telefono=dataClienteInfo["telefono"],
                            correo=dataClienteInfo["correo"],
                            is_main=True
                        )

                        cliente = ClienteInfo.objects.get(
                            id=clienteInfo.id
                        ).cliente
                        serializer = self.get_serializer(
                            cliente
                        )

                        return Response(
                            # data={"response": "Success"},
                            data=serializer.data,
                            status=status.HTTP_201_CREATED
                        )
                    else:
                        notTheSame = True
                else:
                    notTheSame = True

                if notTheSame:
                    cliente = serializer_cliente.save()
                    try:
                        clienteInfo = ClienteInfo.objects.create(
                            cliente=cliente,
                            telefono=dataClienteInfo["telefono"],
                            correo=dataClienteInfo["correo"],
                            is_main=True
                        )
                    except Exception:
                        Cliente.objects.filter(id=cliente.id).delete()
                        return Response(status=status.HTTP_400_BAD_REQUEST)

                    cdata = serializers.CreateClienteSerializer(
                        cliente
                    ).data
                    cdata['clienteInfo'] = serializers.ClienteInfoSerializer(
                        clienteInfo
                    ).data

                    # Call SSOT
                    url = (
                        'https://signonservice-difbz2ztya-uc.a.run.app/newuser'
                    )
                    headers = {
                        "Content-Type": "application/json"
                    }
                    status_code = 200
                    data = {
                        "uid": str(cliente.id),
                        "password": request.data.get('contrasena')
                    }
                    SSOT = call_me.maybe(
                        url,
                        headers,
                        data,
                        status_code
                    )

                    if SSOT:
                        # Call MKT
                        url = 'https://diz-marketing.herokuapp.com/NEW_USER'
                        headers = {
                            "Content-Type": "application/json"
                        }
                        status_code = 200
                        data = {
                            "nombrePila": dataCliente["nombrePila"],
                            "correo": dataClienteInfo["correo"]
                        }
                        call_me.maybe(
                            url,
                            headers,
                            data,
                            status_code
                        )
                    else:
                        cliente.delete()
                        return Response(
                            data={"Response": "SSOT_FAILED"},
                            status=status.HTTP_417_EXPECTATION_FAILED
                        )

                    return Response(
                            data=cdata,
                            status=status.HTTP_201_CREATED
                        )
            else:
                if not validName:
                    return Response(
                        data={"Response": "NOT A CORRECT NAME"},
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
                if not check:
                    return Response(
                        data={"Response": "NOT A CORRECT PHONE"},
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
                if not check1:
                    return Response(
                        data={"Response": "EMAIL ALREADY IN USE"},
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
                if not check2:
                    return Response(
                        data={"Response": "NOT AN EMAIL"},
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
                if not checkGender:
                    return Response(
                        data={"Response": "GENDER PROBABLY INCORRECT"},
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            cliente = self.get_object()
            serializer = serializers.ClienteSerializer(cliente)
            data = serializer.data
        except Exception:
            return Response(
                data={"Response": "NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            data=data,
            status=status.HTTP_302_FOUND
        )

    def update(self, request, *args, **kwargs):
        try:
            cliente = self.get_object()
        except Exception:
            return Response(
                data={"Response": "NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            new_cliente_info = request.data.get('clienteInfo')
        except Exception:
            return Response(
                data={"Response": "BAD_REQUEST"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            clienteInfo = ClienteInfo.objects.create(
                cliente=cliente,
                telefono=new_cliente_info['telefono'],
                correo=new_cliente_info['correo'],
                calle=new_cliente_info['calle'],
                colonia=new_cliente_info['colonia'],
                ciudad=new_cliente_info['ciudad'],
                cp=new_cliente_info['cp'],
                estado=new_cliente_info['estado'],
                entreCalles=new_cliente_info['entreCalles']
            )
        except Exception:
            return Response(
                data={"Response": "BAD_REQUEST"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = serializers.ClienteInfoSerializer(
            clienteInfo
        ).data
        serializer['id'] = clienteInfo.cliente.id

        return Response(
            data=serializer,
            status=status.HTTP_201_CREATED
        )

    def partial_update(self, request, *args, **kwargs):
        try:
            cliente = self.get_object()
            clienteInfo = ClienteInfo.objects.get(
                cliente=cliente,
                is_main=True
            )
        except Exception:
            return Response(
                data={"Response": "NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            new_cliente = request.data.get('cliente')
            new_cliente_info = request.data.get('clienteInfo')
        except Exception:
            return Response(
                data={"Response": "BAD_REQUEST"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cliente.nombrePila = new_cliente["nombrePila"]
        except Exception:
            cliente.nombrePila = cliente.nombrePila

        try:
            cliente.apellidoPat = new_cliente["apellidoPat"]
        except Exception:
            cliente.apellidoPat = cliente.apellidoPat

        try:
            cliente.apellidoMat = new_cliente["apellidoMat"]
        except Exception:
            cliente.apellidoMat = cliente.apellidoMat

        try:
            cliente.fechaNac = new_cliente["fechaNac"]
        except Exception:
            cliente.fechaNac = cliente.fechaNac

        try:
            cliente.genero = new_cliente["genero"]
        except Exception:
            cliente.genero = cliente.genero
        cliente.save()
        cliente_data = serializers.CreateClienteSerializer(
            cliente
        ).data

        try:
            clienteInfo.telefono = new_cliente_info["telefono"]
        except Exception:
            clienteInfo.telefono = clienteInfo.telefono

        try:
            clienteInfo.correo = new_cliente_info["correo"]
        except Exception:
            clienteInfo.correo = clienteInfo.correo

        try:
            clienteInfo.calle = new_cliente_info["calle"]
        except Exception:
            clienteInfo.calle = clienteInfo.calle

        try:
            clienteInfo.colonia = new_cliente_info["colonia"]
        except Exception:
            clienteInfo.colonia = clienteInfo.colonia

        try:
            clienteInfo.ciudad = new_cliente_info["ciudad"]
        except Exception:
            clienteInfo.ciudad = clienteInfo.ciudad

        try:
            clienteInfo.cp = new_cliente_info["cp"]
        except Exception:
            clienteInfo.cp = clienteInfo.cp

        try:
            clienteInfo.estado = new_cliente_info["estado"]
        except Exception:
            clienteInfo.estado = clienteInfo.estado

        try:
            clienteInfo.entreCalles = new_cliente_info["entreCalles"]
        except Exception:
            clienteInfo.entreCalles = clienteInfo.entreCalles
        clienteInfo.save()
        cliente_data['clienteInfo'] = serializers.ClienteInfoSerializer(
            clienteInfo
        ).data

        return Response(
            data=cliente_data,
            status=status.HTTP_202_ACCEPTED
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


class CarritoViewSet(viewsets.GenericViewSet):
    'List, create, retreive, update or delete carritos'
    queryset = Carrito.objects.all()
    serializer_class = serializers.CarritoSerializer

    def Duplicate(self, id):
        try:
            Carrito.objects.get(cliente_id=id)
            return True
        except Carrito.DoesNotExist:
            return False

    def create(self, request, *args, **kwargs):
        id = request.data.get('id')
        try:
            cliente = Cliente.objects.get(id=id, is_deleted=False)
        except Exception:
            return Response(
                data={"Response": "NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            duplicate = self.Duplicate(request.data.get('id'))
            if duplicate:
                Carrito.objects.get(cliente_id=id).delete()
            carrito = Carrito.objects.create(
                cliente=cliente
            )
        except Exception:
            return Response(
                data={"Response": "ERROR"},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        for producto in request.data.get('carritoInfo'):
            try:
                CarritoInfo.objects.create(
                    carrito=carrito,
                    codigoProducto=producto["codigoProducto"],
                    cantidadProducto=producto["cantidadProducto"]
                )
            except Exception:
                return Response(
                    data={"Response": "ERROR"},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )

        serializer = self.get_serializer(carrito)

        # Call MKT
        url = 'https://diz-marketing.herokuapp.com/ITEMS_LEFT'
        headers = {
            "Content-Type": "application/json"
        }
        status_code = 200
        data = serializer.data
        data['email'] = ClienteInfo.objects.get(
            cliente=cliente,
            is_main=True
        ).correo
        data['name'] = cliente.nombrePila
        print(data)
        call_me.maybe(
            url,
            headers,
            data,
            status_code
        )

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, *args, **kwargs):
        try:
            carrito = self.get_object()
            cliente = carrito.cliente
            if not cliente.is_deleted:
                serializer = serializers.CarritoSerializer(carrito)
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


class CodigoPostalRetrieveView(viewsets.GenericViewSet):
    queryset = CodigoPostal.objects.all()
    serializer_class = serializers.CodigoPostalSerializer

    def list(self, request, *args, **kwargs):
        codigo = self.request.GET.get('cp')
        try:
            codigoPostal = CodigoPostal.objects.filter(
                codigo=codigo
            )
            if codigoPostal.exists():
                serializer = self.get_serializer(
                    codigoPostal,
                    many=True
                )
                return Response(
                    data=serializer.data,
                    status=status.HTTP_302_FOUND
                )
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
