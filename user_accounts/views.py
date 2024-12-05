from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer
import random
import string
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import AccountDetails, PaymentMethod, OrderHistory, Settings, Address
from .serializers import (
    AccountDetailsSerializer,
    PaymentMethodSerializer,
    OrderHistorySerializer,
    SettingsSerializer,
    AddressSerializer,
)

User = get_user_model()


class AccountDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "name": user.username,
            "email": user.email,
        })
    
@api_view(['POST'])
def signup(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    # Debug: Check if we are getting the username and password correctly
    print(f"Username: {username}, Password: {password}")
    
    user = authenticate(request, username=username, password=password)
    
    # Debug: Check the user object
    print(f"Authenticated User: {user}")
    
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': username,
        }, status=status.HTTP_200_OK)
        # return Response({"token": token.key, "user": username}, status=status.HTTP_200_OK)
    
    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')
    user = User.objects.filter(email=email).first()
    if user:
        # Generate a random temporary password
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user.set_password(temp_password)
        user.save()
        
        # Send the temporary password to user's email
        send_mail(
            'Password Reset',
            f'Your temporary password is: {temp_password}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
        return Response({"message": "Temporary password sent to your email."}, status=status.HTTP_200_OK)
    return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)

class AccountDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account = AccountDetails.objects.get(user=request.user)
        serializer = AccountDetailsSerializer(account)
        return Response(serializer.data)

class PaymentMethodsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = PaymentMethod.objects.filter(user=request.user)
        serializer = PaymentMethodSerializer(payments, many=True)
        return Response(serializer.data)

class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = OrderHistory.objects.filter(user=request.user)
        serializer = OrderHistorySerializer(orders, many=True)
        return Response(serializer.data)

class SettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        settings = Settings.objects.get(user=request.user)
        serializer = SettingsSerializer(settings)
        return Response(serializer.data)

class AddressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)
