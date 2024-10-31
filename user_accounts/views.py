from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, UserSerializer
import random
import string

User = get_user_model()

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
    user = authenticate(request, username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
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

