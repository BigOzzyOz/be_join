from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import generics, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from user_auth_app.api.serializers import RegisterSerializer
from user_auth_app.models import ProfileUser


class UserLoginView(ObtainAuthToken):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            data["name"] = f"{user.first_name} {user.last_name}"
            data["username"] = user.username
            data["email"] = user.email
            data["token"] = token.key
            data["id"] = ProfileUser.objects.get(user=user).id
        else:
            data = serializer.errors
        status_code = status.HTTP_201_CREATED if serializer.is_valid() else status.HTTP_400_BAD_REQUEST
        return Response(data, status=status_code)


class GuestUserView(ObtainAuthToken):
    permission_classes = (AllowAny,)

    def post(self, request):
        with transaction.atomic():
            guest_user, created_user = User.objects.select_for_update().get_or_create(
                username="guest", defaults={"password": "guest"}
            )
            if created_user:
                guest_user.set_password("guest")
                guest_user.save()
            token, created_token = Token.objects.get_or_create(user=guest_user)

        data = {
            "username": guest_user.username,
            "email": guest_user.email,
            "token": token.key,
            "id": ProfileUser.objects.get(user=guest_user).id,
        }
        status_code = status.HTTP_201_CREATED if created_user or created_token else status.HTTP_200_OK
        return Response(data, status=status_code)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            data = {
                "username": user.username,
                "email": user.email,
                "token": token.key,
                "name": f"{user.first_name} {user.last_name}",
                "id": ProfileUser.objects.get(user=user).id,
            }
        else:
            data = serializer.errors
        status_code = status.HTTP_201_CREATED if serializer.is_valid() else status.HTTP_400_BAD_REQUEST
        return Response(data, status=status_code)
