from django.urls import path
from .views import GuestUserView, UserLoginView, UserRegistrationView, CheckAuthStatusView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("register/", UserRegistrationView.as_view(), name="user_register"),
    path("guest/", GuestUserView.as_view(), name="user_guest"),
    path("status/", CheckAuthStatusView.as_view(), name="auth_status"),
]
