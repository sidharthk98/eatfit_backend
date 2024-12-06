from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class DummyTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the token from the Authorization header
        auth = request.headers.get('Authorization')

        if not auth:
            return None

        # Check if the Authorization header contains the Bearer token
        parts = auth.split()

        if len(parts) != 2 or parts[0].lower() != 'bearer':
            raise AuthenticationFailed('Authorization header must be Bearer token.')

        token = parts[1]

        # Check if the token matches the dummy token
        if token != "dummyToken":
            raise AuthenticationFailed('Invalid token.')

        # If token matches, return a dummy user and None (since we're not actually validating a real user here)
        # You can return a user object if required, but for now, we return `None`.
        return (None, None)
