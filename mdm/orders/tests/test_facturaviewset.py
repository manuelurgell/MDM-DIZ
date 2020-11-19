""" Tests for users of mdm."""
import datetime

from django.test import TestCase

from mdm.clients.models import Cliente
from mdm.orders.models import Compra, Factura
from mdm.orders.views import FacturaViewSet


class DuplicateTestCase(TestCase):
    """Test Duplicate function."""
    def setUp(self):
        cliente = Cliente.objects.create(
            nombrePila='Test Cliente',
            fechaNac=datetime.date.today()
        )
        self.compra = Compra.objects.create(
            cliente=cliente,
            noTarjeta="4152313638174545",
            mesTarjeta="10",
            anioTarjeta="21"
        )

    def test_does_not_exist(self):
        """Test new factura."""
        compra = self.compra

        self.assertEqual(
            FacturaViewSet.Duplicate(self, compra),
            False
        )

    def test_is_duplicate(self):
        """Test duplicate factura."""
        compra = self.compra

        Factura.objects.create(
            compra=compra
        )

        self.assertEqual(
            FacturaViewSet.Duplicate(self, compra),
            True
        )
