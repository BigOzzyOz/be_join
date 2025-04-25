from contacts_app.models import Contact


class AuthUserResponseMixin:
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
