""" Tests for users of mdm."""
import datetime

from django.db import transaction
from django.db.utils import DataError, IntegrityError
from django.test import TestCase

from mdm.clients.models import (
    Cliente,
    ClienteInfo,
    NameException
)


class NameExceptionTestCase(TestCase):
    """Test NameException model."""
    def setUp(self):
        self.nexcept = NameException.objects.create(
            nombre='Test name exception'
        )

    def test_max_length(self):
        """Test max_length values."""
        nexcept = self.nexcept
        with transaction.atomic():
            nexcept.nombre = 'x'*51
            with self.assertRaises(DataError):
                nexcept.save()

    def test_not_nulls(self):
        """Test not_null fields."""
        nexcept = self.nexcept

        with transaction.atomic():
            nexcept.nombre = None
            with self.assertRaises(IntegrityError):
                nexcept.save()


class ClienteTestCase(TestCase):
    """Test Cliente model."""
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombrePila='Test name exception',
            fechaNac=datetime.date.today()
        )

    def test_max_length(self):
        """Test max_length values."""
        cliente = self.cliente
        with transaction.atomic():
            cliente.nombrePila = 'x'*31
            with self.assertRaises(DataError):
                cliente.save()

        with transaction.atomic():
            cliente.apellidoPat = 'x'*31
            with self.assertRaises(DataError):
                cliente.save()

        with transaction.atomic():
            cliente.apellidoMat = 'x'*31
            with self.assertRaises(DataError):
                cliente.save()

        with transaction.atomic():
            cliente.genero = 'x'*31
            with self.assertRaises(DataError):
                cliente.save()

    def test_not_nulls(self):
        """Test not_null fields."""
        cliente = self.cliente

        with transaction.atomic():
            cliente.nombrePila = None
            with self.assertRaises(IntegrityError):
                cliente.save()

        with transaction.atomic():
            cliente.apellidoPat = None
            with self.assertRaises(IntegrityError):
                cliente.save()

        with transaction.atomic():
            cliente.apellidoMat = None
            with self.assertRaises(IntegrityError):
                cliente.save()

        with transaction.atomic():
            cliente.fechaNac = None
            with self.assertRaises(IntegrityError):
                cliente.save()

        with transaction.atomic():
            cliente.genero = None
            with self.assertRaises(IntegrityError):
                cliente.save()

        with transaction.atomic():
            cliente.created_date = None
            with self.assertRaises(IntegrityError):
                cliente.save()

        with transaction.atomic():
            cliente.is_deleted = None
            with self.assertRaises(IntegrityError):
                cliente.save()

    # def test_created_date(self):
    #     """Test created_date field."""
    #     cliente = self.cliente
    #     self.assertEqual(datetime.date.today(), cliente.created_date.date())

    def test_defaults(self):
        """Test default values."""
        cliente = self.cliente
        self.assertEqual(cliente.is_deleted, False)


class ClienteInfoTestCase(TestCase):
    """Test ClienteInfo model."""
    def setUp(self):
        cliente = Cliente.objects.create(
            nombrePila='Test Cliente',
            fechaNac=datetime.date.today()
        )
        self.clienteInfo = ClienteInfo.objects.create(
            cliente=cliente
        )

    def test_length(self):
        """Test max_length values."""
        clienteInfo = self.clienteInfo
        with transaction.atomic():
            clienteInfo.telefono = 'x'*13
            with self.assertRaises(DataError):
                clienteInfo.save()

        with transaction.atomic():
            clienteInfo.correo = 'x'*31
            with self.assertRaises(DataError):
                clienteInfo.save()

        with transaction.atomic():
            clienteInfo.calle = 'x'*51
            with self.assertRaises(DataError):
                clienteInfo.save()

        with transaction.atomic():
            clienteInfo.colonia = 'x'*51
            with self.assertRaises(DataError):
                clienteInfo.save()

        with transaction.atomic():
            clienteInfo.ciudad = 'x'*51
            with self.assertRaises(DataError):
                clienteInfo.save()

        with transaction.atomic():
            clienteInfo.cp = 'x'*11
            with self.assertRaises(DataError):
                clienteInfo.save()

        with transaction.atomic():
            clienteInfo.estado = 'x'*51
            with self.assertRaises(DataError):
                clienteInfo.save()

        with transaction.atomic():
            clienteInfo.entreCalles = 'x'*51
            with self.assertRaises(DataError):
                clienteInfo.save()

    def test_not_nulls(self):
        """Test not_null fields."""
        clienteInfo = self.clienteInfo

        with transaction.atomic():
            clienteInfo.cliente = None
            with self.assertRaises(IntegrityError):
                clienteInfo.save()

        with transaction.atomic():
            clienteInfo.is_main = None
            with self.assertRaises(IntegrityError):
                clienteInfo.save()

    def test_nulls(self):
        """Test null fields."""
        clienteInfo = self.clienteInfo

        clienteInfo.telefono = None
        clienteInfo.save()
        self.assertEqual(clienteInfo.telefono, None)

        clienteInfo.correo = None
        clienteInfo.save()
        self.assertEqual(clienteInfo.correo, None)

        clienteInfo.calle = None
        clienteInfo.save()
        self.assertEqual(clienteInfo.calle, None)

        clienteInfo.colonia = None
        clienteInfo.save()
        self.assertEqual(clienteInfo.colonia, None)

        clienteInfo.ciudad = None
        clienteInfo.save()
        self.assertEqual(clienteInfo.ciudad, None)

        clienteInfo.cp = None
        clienteInfo.save()
        self.assertEqual(clienteInfo.cp, None)

        clienteInfo.estado = None
        clienteInfo.save()
        self.assertEqual(clienteInfo.estado, None)

        clienteInfo.entreCalles = None
        clienteInfo.save()
        self.assertEqual(clienteInfo.entreCalles, None)

    def test_defaults(self):
        """Test default values."""
        clienteInfo = self.clienteInfo
        self.assertEqual(clienteInfo.telefono, '')
        self.assertEqual(clienteInfo.correo, '')
        self.assertEqual(clienteInfo.calle, '')
        self.assertEqual(clienteInfo.colonia, '')
        self.assertEqual(clienteInfo.ciudad, '')
        self.assertEqual(clienteInfo.cp, '')
        self.assertEqual(clienteInfo.estado, '')
        self.assertEqual(clienteInfo.entreCalles, '')
        self.assertEqual(clienteInfo.is_main, False)

    def test_on_delete(self):
        """Test on_delete constraints (CASCADE)."""
        cliente = Cliente.objects.create(
            nombrePila='Test Cliente',
            fechaNac=datetime.date.today()
        )
        clienteInfo = ClienteInfo.objects.create(
            cliente=cliente
        )
        cliente.delete()
        clienteInfo_qs = ClienteInfo.objects.filter(pk=clienteInfo.pk)
        self.assertEqual(clienteInfo_qs.exists(), False)

        # Once the constraint was tested, delete qs
        # to avoid Exception on tear_down()
        clienteInfo_qs.delete()
