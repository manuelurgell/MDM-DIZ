""" Tests for users of mdm."""
import datetime

from django.db import transaction
from django.test import TestCase

from mdm.clients.models import (
    Cliente,
    ClienteInfo,
    NameException
)
from mdm.clients.views import ClientViewSet


class ValidateNameTestCase(TestCase):
    """Test ValidateName function."""
    def setUp(self):
        self.nexcept = NameException.objects.create(
            nombre='Test name exception'
        )

    def test_is_valid(self):
        """Test valid-name."""
        self.assertEqual(
            ClientViewSet.ValidateName(self, 'Manuel'),
            True
        )

    def test_is_not_valid(self):
        """Test non-valid name."""
        self.assertEqual(
            ClientViewSet.ValidateName(self, 'X Æ A-12'),
            False
        )

    def test_is_valid_on_except(self):
        """Test non-valid name on Exceptions table."""
        nexcept = self.nexcept
        with transaction.atomic():
            nexcept.nombre = 'X Æ A-12'
            nexcept.save()
            self.assertEqual(
                ClientViewSet.ValidateName(self, 'X Æ A-12'),
                True
            )


class DuplicateTestCase(TestCase):
    """Test Duplicate function."""
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombrePila='Test Cliente',
            fechaNac=datetime.date.today()
        )
        self.clienteInfo = ClienteInfo.objects.create(
            cliente=self.cliente
        )

    def test_is_duplicate(self):
        """Test duplicate email."""
        clienteInfo = self.clienteInfo
        with transaction.atomic():
            clienteInfo.correo = 'example@correo.com'
            clienteInfo.save()

        self.assertEqual(
            ClientViewSet.Duplicate(self, 'example@correo.com'),
            False
        )

    def test_is_not_duplicate_clienteInfo(self):
        """Test not duplicate email because is new."""
        self.assertEqual(
            ClientViewSet.Duplicate(self, 'example@correo.com'),
            True
        )

    def test_is_not_duplicate_cliente(self):
        """Test not duplicate email because cliente is_deleted."""
        cliente = self.cliente
        clienteInfo = self.clienteInfo

        with transaction.atomic():
            clienteInfo.correo = 'example@correo.com'
            clienteInfo.save()

        with transaction.atomic():
            cliente.is_deleted = True
            cliente.save()

        self.assertEqual(
            ClientViewSet.Duplicate(self, 'example@correo.com'),
            True
        )


class ValidatePhoneTestCase(TestCase):
    """Test ValidatePhone function."""
    def setUp(self): None

    def test_is_valid_mex(self):
        """Test MX phone is_valid."""
        self.assertEqual(
            ClientViewSet.ValidatePhone(self, '7224123456'),
            True
        )

    def test_is_valid_int(self):
        """Test MX phone is_valid."""
        self.assertEqual(
            ClientViewSet.ValidatePhone(self, '442083661177'),
            True
        )

    def test_is_not_possible(self):
        """Test phone not is_possible."""
        self.assertEqual(
            ClientViewSet.ValidatePhone(self, '911'),
            False
        )

    def test_is_not_valid_mex(self):
        """Test MX phone not is_valid."""
        self.assertEqual(
            ClientViewSet.ValidatePhone(self, '1111111111'),
            False
        )

    def test_is_not_valid_int(self):
        """Test int phone not is_valid."""
        self.assertEqual(
            ClientViewSet.ValidatePhone(self, '12001230101'),
            False
        )


class ValidateEmailTestCase(TestCase):
    """Test ValidateEmail function."""
    def setUp(self): None

    def test_is_valid(self):
        """Test email is_valid."""
        self.assertEqual(
            ClientViewSet.ValidateEmail(self, 'correo@example.com'),
            True
        )

    def test_is_not_valid(self):
        """Test email not is_valid."""
        self.assertEqual(
            ClientViewSet.ValidateEmail(self, 'correoexample.com'),
            False
        )
        self.assertEqual(
            ClientViewSet.ValidateEmail(self, 'correo@examplecom'),
            False
        )
        self.assertEqual(
            ClientViewSet.ValidateEmail(self, 'correo@example.'),
            False
        )


class ValidateGenreTestCase(TestCase):
    """Test validateGenre function."""
    def setUp(self): None

    def test_is_valid(self):
        """Test genre is_valid."""
        self.assertEqual(
            ClientViewSet.validateGender(self, 'Melisa', 'M'),
            True
        )
        self.assertEqual(
            ClientViewSet.validateGender(self, 'EMILIANO', 'H'),
            True
        )
        self.assertEqual(
            ClientViewSet.validateGender(self, 'Jose Maria', 'O'),
            True
        )

    def test_is_not_valid(self):
        """Test genre not is_valid."""
        self.assertEqual(
            ClientViewSet.validateGender(self, 'Mario', 'Hombre'),
            False
        )
        self.assertEqual(
            ClientViewSet.validateGender(self, 'Melisa', 'H'),
            False
        )
        self.assertEqual(
            ClientViewSet.validateGender(self, 'Emiliano', 'M'),
            False
        )
