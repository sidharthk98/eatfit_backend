from django.urls import path
from .views import signup, login, forgot_password
from .views import (
    AccountDetailsView,
    PaymentMethodsView,
    OrderHistoryView,
    SettingsView,
    AddressView,
)

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path("account-details/", AccountDetailsView.as_view(), name="account_details"),
    path("payment-methods/", PaymentMethodsView.as_view(), name="payment_methods"),
    path("order-history/", OrderHistoryView.as_view(), name="order_history"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("addresses/", AddressView.as_view(), name="addresses"),
]