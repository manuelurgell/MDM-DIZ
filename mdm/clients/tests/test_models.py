""" Tests for users of mdm."""
# import datetime
from django.db import transaction
from django.db.utils import DataError
from django.test import TestCase

from mdm.clients.models import NameException


class NameExceptionTestCase(TestCase):
    """Test NameException model."""
    def setUp(self):
        self.nexcept = NameException.objects.create(
            nombre='Test name exception'
        )

    def test_length(self):
        """Test max_length values."""
        nexcept = self.nexcept
        with transaction.atomic():
            nexcept.nombre = 'x'*51
            with self.assertRaises(DataError):
                nexcept.save()
