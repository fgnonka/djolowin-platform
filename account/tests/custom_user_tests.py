from django.test import TestCase
from django.urls import reverse
from django.core import mail
from decimal import Decimal

from account.models import CustomUser, Address
from wallet.models import UserWallet


class CustomUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = CustomUser.objects.create_user(
            email="testuser@example.com", password="testpass"
        )
        cls.address = Address.objects.create(
            first_name="Test",
            last_name="User",
            address="123 Main St",
            city="Anytown",
            state="CA",
            country="US",
            postal_code="12345",
        )
        cls.user.default_billing_address = cls.address
        cls.user.save()

    def test_full_name(self):
        self.assertEqual(self.user.get_full_name, "testuser@example.com")

    def test_address_full_name(self):
        self.assertEqual(self.address.full_name, "Test User")

    def test_address_as_data(self):
        self.assertEqual(
            self.address.as_data(),
            {
                "first_name": "Test",
                "last_name": "User",
                "address": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "country": "US",
                "postal_code": "12345",
            },
        )

    def test_get_wallet(self):
        # Check if a wallet already exists for the user
        try:
            wallet = self.user.get_wallet
        except UserWallet.DoesNotExist:
            # Create a new wallet for the user
            wallet = UserWallet.objects.create(user=self.user, balance=Decimal(0))
        self.assertEqual(self.user.get_wallet, wallet)

    def test_email_user(self):
        # Send message.
        self.user.email_user("Subject here", "Here is the message.", "from@example.com")
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        # Verify that the message subject and body are correct.
        self.assertEqual(mail.outbox[0].subject, "Subject here")
        self.assertEqual(mail.outbox[0].body, "Here is the message.")
        self.assertEqual(mail.outbox[0].from_email, "from@example.com")
        self.assertEqual(mail.outbox[0].to, ["testuser@example.com"])

    def test_absolute_url(self):
        url = reverse("account:user-detail", kwargs={"username": self.user.username})
        self.assertEqual(self.user.get_absolute_url(), url)
