import datetime

from rest_framework import status, viewsets
from rest_framework.response import Response

from mdm.clients.models import Cliente
# , ClienteInfo
from mdm.orders import serializers
from mdm.orders.models import Compra, Factura, Pedido
# from mdm.utils import call_me

# Create your views here.


class CompraViewSet(viewsets.ModelViewSet):
    '''List, create, retrieve, update, partial_update or delete compras'''
    queryset = Compra.objects.all()
    serializer_class = serializers.CompraSerializer

    def create(self, request, *args, **kwargs):
        try:
            cliente = Cliente.objects.get(
                id=request.data.get('id'),
                is_deleted=False
            )
        except Exception:
            return Response(
                data={"Response": "NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            dataCompra = request.data.get('compra')
            dataPedido = request.data.get('pedido')
        except Exception:
            return Response(
                data={"Response": "NOT_ACCEPTABLE"},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        try:
            compra = Compra.objects.create(
                cliente=cliente,
                noTarjeta=dataCompra["noTarjeta"],
                mesTarjeta=dataCompra["mesTarjeta"],
                anioTarjeta=dataCompra["anioTarjeta"],
                total=dataCompra["total"],
                calle=dataCompra["calle"],
                numero=dataCompra["numero"],
                colonia=dataCompra["colonia"],
                ciudad=dataCompra["ciudad"],
                cp=dataCompra["cp"],
                estado=dataCompra["estado"],
                entreCalles=dataCompra["entreCalles"]
            )
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        for producto in dataPedido:
            try:
                Pedido.objects.create(
                    compra=compra,
                    codigoProducto=producto["codigoProducto"],
                    cantidadProducto=producto["cantidadProducto"],
                    precioProducto=producto["precioProducto"]
                )
            except Exception:
                return Response(
                    data={"Response": "ERROR"},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )

            serializer = self.get_serializer(compra)

            """
            # Call LOG
            url = 'https://logistica-294123.uc.r.appspot.com/generate'
            headers = {
                "Content-Type": "application/json"
            }
            status_code = 200
            data = serializer.data
            clienteInfo = ClienteInfo.objects.get(
                cliente=cliente,
                is_main=True
            )
            data['name'] = cliente.nombrePila
            data['email'] = clienteInfo.correo
            print(data)
            call_LOG = call_me.maybe(
                url,
                headers,
                data,
                status_code
            )

            if not call_LOG:
                compra.delete()
                return Response(
                    data={"Response": "LOGISTICS_FAILED"},
                    status=status.HTTP_417_EXPECTATION_FAILED
                )
            """

            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            cliente = Cliente.objects.get(id=self.kwargs['pk'])
            if not cliente.is_deleted:
                serializer = serializers.ClienteSerializer(cliente)
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


class FacturaViewSet(viewsets.ModelViewSet):
    '''List, create, retrieve, update, partial_update or delete compras'''
    queryset = Factura.objects.all()
    serializer_class = serializers.FacturaSerializer

    def Duplicate(self, compra):
        try:
            Factura.objects.get(compra=compra)
            return True
        except Factura.DoesNotExist:
            return False

    def create(self, request, *args, **kwargs):
        data = request.data
        compra_id = data["compra_id"]
        try:
            compra = Compra.objects.get(
                id=compra_id
            )
        except Exception:
            return Response(
                data={"Response": "NOT_FOUND"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            duplicate = self.Duplicate(compra)
            if duplicate:
                factura = Factura.objects.get(compra=compra)
            else:
                factura = Factura.objects.create(
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
                    entreCalles=data["entreCalles"],
                    compra=compra,
                )
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(factura)

        # Call MKT
        # url = 'https://diz-marketing.herokuapp.com/NEW_PURCHASE'
        # headers = {
        #     "Content-Type": "application/json"
        # }
        # status_code = 200
        # data = {
        #     serializer.data
        # }
        # call_me.maybe(
        #     url,
        #     headers,
        #     data,
        #     status_code
        # )

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


class ValidateCardView(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = serializers.ClienteSerializer

    def evenDigits(self, card, length, end):
        sum = 0
        for i in range(length-2, end, -2):
            number = eval(card[i])
            number = number * 2
            if number > 9:
                strNumber = str(number)
                number = eval(strNumber[0]) + eval(strNumber[1])
            sum += number
        return sum

    def oddDigits(self, card, length, end):
        sumOdd = 0
        for i in range(length-3, end, -2):
            sumOdd += eval(card[i])
        return sumOdd

    def card_luhn(self, card):
        length = len(card)
        if length == 16:
            sumEven = self.evenDigits(card, length, -1)
            sumOdd = self.oddDigits(card, length, 0)
            total = sumEven + sumOdd + int(card[15])
            if total % 10 == 0:
                return True
            else:
                return False
        elif length == 15:
            sumEven = self.evenDigits(card, length, 0)
            sumOdd = self.oddDigits(card, length, -1)
            total = sumEven + sumOdd + int(card[14])
            if total % 10 == 0:
                return True
            else:
                return False
        else:
            return False

    def expired_card(self, monthC, yearC):
        year = datetime.datetime.today().year
        currentMonth = datetime.datetime.today().month
        currentYear = int(str(year)[2] + str(year)[3])
        if monthC > currentMonth:
            if yearC >= currentYear:
                return True
            else:
                return False
        else:
            if yearC > currentYear:
                return True
            else:
                return False

    def create(self, request, *args, **kwargs):
        noTarjeta = request.data.get('noTarjeta')
        mesTarjeta = request.data.get('mesTarjeta')
        anioTarjeta = request.data.get('anioTarjeta')

        checkTarjeta = self.card_luhn(noTarjeta)
        checkExpired = self.expired_card(int(mesTarjeta), int(anioTarjeta))

        if checkTarjeta and checkExpired:
            return Response(
                data={
                    "noTarjeta": noTarjeta,
                    "mesTarjeta": mesTarjeta,
                    "anioTarjeta": anioTarjeta
                },
                status=status.HTTP_202_ACCEPTED
            )
        else:
            if not checkTarjeta:
                return Response(
                    data={"Response": "CARD_NOT_VALID"},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )
            if not checkExpired:
                return Response(
                    data={"Response": "EXPIRED_CARD"},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )

            return Response(
                    data={"Response": "ERROR"},
                    status=status.HTTP_400_BAD_REQUEST
                )
