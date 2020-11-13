""" Tests for users of mdm."""
# import datetime
from django.db import transaction
from django.test import TestCase

from mdm.clients.models import NameException
from mdm.clients.views import ClientViewSet


class ValidateNameTestCase(TestCase):
    """Test ValidateName function."""
    def setUp(self):
        self.nexcept = NameException.objects.create(
            nombre='Test name exception'
        )

    def test_is_valid(self):
        """Test max_length values."""
        self.assertEqual(
            ClientViewSet.ValidateName(self, 'Manuel'),
            True
        )

    def test_is_not_valid(self):
        """Test max_length values."""
        self.assertEqual(
            ClientViewSet.ValidateName(self, 'X Æ A-12'),
            False
        )

    def test_is_valid_on_except(self):
        """Test max_length values."""
        nexcept = self.nexcept
        with transaction.atomic():
            nexcept.nombre = 'X Æ A-12'
            nexcept.save()
            self.assertEqual(
                ClientViewSet.ValidateName(self, 'X Æ A-12'),
                True
            )
