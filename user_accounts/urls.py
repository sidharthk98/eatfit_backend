from django.urls import path
from .views import signup, login, forgot_password

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('forgot-password/', forgot_password, name='forgot_password'),
]

