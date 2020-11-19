""" Tests for users of mdm."""
import datetime

from django.test import TestCase

from mdm.orders.views import ValidateCardView
# mesTarjeta="10",
# anioTarjeta="21"


class Card_LuhnTestCase(
    TestCase,
    ValidateCardView
):
    """Test card_luhn function."""
    def setUp(self): None

    def test_is_valid(self):
        """Test valid cards."""
        self.assertEqual(
            self.card_luhn("4152313638174545"),
            True
        )
        self.assertEqual(
            self.card_luhn("375987654321301"),
            True
        )

    def test_is_not_valid(self):
        """Test not valid cards."""
        self.assertEqual(
            self.card_luhn("4152313638174546"),
            False
        )
        self.assertEqual(
            self.card_luhn("375987654321302"),
            False
        )
        self.assertEqual(
            self.card_luhn("41523136381745"),
            False
        )
        self.assertEqual(
            self.card_luhn("1234567890123456"),
            False
        )
        self.assertEqual(
            self.card_luhn("123456789012345"),
            False
        )


class Expired_CardTestCase(TestCase):
    """Test expired_card function."""
    def setUp(self): None

    def test_is_valid(self):
        """Test valid cards."""
        year = datetime.datetime.today().year
        self.assertEqual(
            ValidateCardView.expired_card(
                self,
                datetime.datetime.today().month+1,
                int(str(year)[2] + str(year)[3])
            ),
            True
        )
        self.assertEqual(
            ValidateCardView.expired_card(
                self,
                datetime.datetime.today().month,
                int(str(year+1)[2] + str(year+1)[3])
            ),
            True
        )

    def test_is_not_valid(self):
        """Test not valid cards."""
        year = datetime.datetime.today().year
        self.assertEqual(
            ValidateCardView.expired_card(
                self,
                datetime.datetime.today().month+1,
                int(str(year-1)[2] + str(year-1)[3])
            ),
            False
        )
        self.assertEqual(
            ValidateCardView.expired_card(
                self,
                datetime.datetime.today().month,
                int(str(year)[2] + str(year)[3])
            ),
            False
        )
