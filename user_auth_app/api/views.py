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
            data["username"] = user.username
            data["email"] = user.email
            data["token"] = token.key
            data["id"] = ProfileUser.objects.get(user=user).id
        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED if serializer.is_valid() else status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            data = {"username": user.username, "email": user.email, "token": token.key}
        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED if serializer.is_valid() else status.HTTP_400_BAD_REQUEST)
