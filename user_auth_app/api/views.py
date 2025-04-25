"""
API views for user authentication: login, guest login, registration, and auth status check.
"""

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from user_auth_app.api.serializers import RegisterSerializer
from user_auth_app.api.mixins import AuthUserResponseMixin


class UserLoginView(AuthUserResponseMixin, ObtainAuthToken):
    """
    API endpoint for user login. Returns token and user info on success.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            data = self._build_user_response(user, token)
        else:
            data = serializer.errors
        status_code = status.HTTP_201_CREATED if serializer.is_valid() else status.HTTP_400_BAD_REQUEST
        return Response(data, status=status_code)


class GuestUserView(AuthUserResponseMixin, ObtainAuthToken):
    """
    API endpoint for guest login. Returns token and guest user info.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        with transaction.atomic():
            guest_user, created_user = User.objects.select_for_update().get_or_create(
                username="guest",
                defaults={"password": "guest", "first_name": "Guest", "last_name": "User", "email": "guest@user.de"},
            )
            if created_user:
                guest_user.set_password("guest")
                guest_user.save()
            token, created_token = Token.objects.get_or_create(user=guest_user)

        data = self._build_user_response(guest_user, token, include_name=False)
        status_code = status.HTTP_201_CREATED if created_user or created_token else status.HTTP_200_OK
        return Response(data, status=status_code)


class UserRegistrationView(AuthUserResponseMixin, generics.CreateAPIView):
    """
    API endpoint for user registration. Returns token and user info on success.
    """

    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            data = self._build_user_response(user, token)
        else:
            data = serializer.errors
        status_code = status.HTTP_201_CREATED if serializer.is_valid() else status.HTTP_400_BAD_REQUEST
        return Response(data, status=status_code)


class CheckAuthStatusView(generics.RetrieveAPIView):
    """
    API endpoint to check if the current user is authenticated.
    """

    permission_classes = (AllowAny,)

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            data = {
                "username": user.username,
                "authenticated": True,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"authenticated": False})
