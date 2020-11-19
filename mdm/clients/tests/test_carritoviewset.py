""" Tests for users of mdm."""
import datetime

from django.test import TestCase

from mdm.clients.models import (
    Carrito,
    Cliente
)
from mdm.clients.views import CarritoViewSet


class DuplicateTestCase(TestCase):
    """Test Duplicate function."""
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombrePila='Test Cliente',
            fechaNac=datetime.date.today()
        )

    def test_does_not_exist(self):
        """Test new carrito."""
        cliente = self.cliente

        self.assertEqual(
            CarritoViewSet.Duplicate(self, cliente.id),
            False
        )

    def test_is_duplicate(self):
        """Test duplicate carrito."""
        cliente = self.cliente

        Carrito.objects.create(
            cliente=self.cliente
        )

        self.assertEqual(
            CarritoViewSet.Duplicate(self, cliente.id),
            True
        )
