from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccountDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="account_details")
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name}'s Account"

class PaymentMethod(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payment_methods")
    card_number = models.CharField(max_length=16)
    expiry_date = models.DateField()

    def __str__(self):
        return f"Payment method for {self.user.name}"

class OrderHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order_history")
    order_id = models.CharField(max_length=50)
    date = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.order_id} for {self.user.name}"

class Settings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="settings")
    notifications = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)

    def __str__(self):
        return f"Settings for {self.user.name}"

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"Address for {self.user.name}"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_student', False)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    # Fields
    user_id = models.AutoField(primary_key=True)  # Auto incrementing user ID
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    billing_address = models.TextField()
    is_student = models.BooleanField(default=False)
    password = models.CharField(max_length=255)
    list_of_orders = models.JSONField(default=list)  # List of order IDs

    # Required for AbstractBaseUser
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']
    
    objects = UserManager()

    # Methods
    def register(self):
        self.save()
    
    def login(self):
        # Custom login logic (could be handled using Django's authenticate system)
        return True  # Placeholder for real login logic
    
    def logout(self):
        pass  # Placeholder for logout logic
    
    def update_profile(self, name=None, phone_number=None, billing_address=None):
        if name:
            self.name = name
        if phone_number:
            self.phone_number = phone_number
        if billing_address:
            self.billing_address = billing_address
        self.save()

    def update_password(self, new_password):
        self.set_password(new_password)
        self.save()

    def remove_payment_method(self, payment):
        if payment in self.payment_methods:
            self.payment_methods.remove(payment)
        self.save()

    def view_order_history(self):
        # Placeholder for order history logic
        return self.list_of_orders