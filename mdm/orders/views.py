from mdm.orders.models import Compra, Pedido, Factura
from mdm.clients.models import ClienteInfo
from mdm.orders import serializers

from rest_framework import status, viewsets
from rest_framework.response import Response

import datetime


# Create your views here.
class CompraViewSet(viewsets.ModelViewSet):
    '''List, create, retrieve, update, partial_update or delete compras'''
    queryset = Compra.objects.all()
    serializer_class = serializers.CompraSerializer

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
        print("impares")
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
        elif length == 15:
            sumEven = self.evenDigits(card, length, 0)
            sumOdd = self.oddDigits(card, length, -1)
            total = sumEven + sumOdd + int(card[14])
            if total % 10 == 0:
                return True

        else:
            return False

    def expired_card(self, monthC, yearC):
        print('chequeo de tarjetas')
        currentYear = datetime.datetime.today().year
        currentMonth = datetime.datetime.today().month
        strYear = str(currentYear)
        year = strYear[0] + strYear[1]
        print(year)
        print(currentMonth)
        if monthC > currentMonth and yearC >= int(year):
            print('buena')
            return True
        elif monthC <= currentMonth and yearC > int(year):
            print('buena')
            return True
        else:
            print('vencida')
            return False

    def create(self, request, *args, **kwargs):
        dataCompra = request.data.get('compra')
        correo = dataCompra["correo"]
        cliente = ClienteInfo.objects.get(
            correo=correo,
            is_main=True
        ).cliente
        tarjeta = dataCompra["noTarjeta"]
        validateCard = self.card_luhn(tarjeta)
        mesT = int(dataCompra["mesTarjeta"])
        anioT = int(dataCompra["anioTarjeta"])
        checkExpired = self.expired_card(mesT, anioT)
        if validateCard and checkExpired:
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
                try:
                    dataPedido = request.data.get('pedido')

                    Pedido.objects.create(
                        compra=compra,
                        codigoProducto=dataPedido["codigoProducto"],
                        cantidadProducto=dataPedido["cantidadProducto"],
                        precioProducto=dataPedido["precioProducto"]
                    )
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
        else:
            if not checkExpired and not validateCard:
                return Response(
                    data={"Response": "CARD NOT VALID AND EXPIRED"},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )
            elif not checkExpired:
                return Response(
                    data={"Response": "EXPIRED_CARD"},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )
            else:
                return Response(
                    data={"Response": "CARD_NOT_VALID"},
                    status=status.HTTP_406_NOT_ACCEPTABLE
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
        pedido = Pedido.objects.filter(compra=compra)
        Factura.objects.create(
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
        dataFactura = {
            "compra": compra,
            "RFC": data["RFC"],
            "razonSocial": data["razonSocial"],
            "correo": data["correo"],
            "telefono": data["telefono"],
            "calle": data["calle"],
            "numero": data["numero"],
            "colonia": data["colonia"],
            "ciudad": data["ciudad"],
            "cp": data["cp"],
            "estado": data["estado"],
            "entreCalles": data["entreCalles"],
            "pedido": pedido
        }
        try:
            serializer = self.get_serializer(dataFactura)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(
            # data={"response": "Success"},
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )
