from django.db import models
from django.contrib.auth.models import User

class AccountDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account_details")
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_methods")
    card_number = models.CharField(max_length=16)
    expiry_date = models.DateField()

class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_history")
    order_id = models.CharField(max_length=50)
    date = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    notifications = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
