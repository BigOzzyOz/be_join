"""
Mixin for building user response dictionaries for authentication endpoints.
"""

from contacts_app.models import Contact


class AuthUserResponseMixin:
    """
    Provides a helper method to build a user/token response for login, registration, and guest endpoints.
    """

    def _build_user_response(self, user, token, include_name=True):
        response = {
            "username": user.username,
            "email": user.email,
            "token": token.key,
            "id": Contact.objects.get(user=user).id,
        }
        if include_name:
            response["name"] = f"{user.first_name} {user.last_name}"
        return response
