"""
Custom permissions for contacts_app API endpoints.
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS
from contacts_app.utils import contact_is_no_user_and_user_not_guest


class IsOwnerOrNonUserOrNotGuest(BasePermission):
    """
    Permission: Allow SAFE_METHODS, owner, or non-user contacts (if user is not guest).
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the request has permission for the given contact object.
        """
        if request.method in SAFE_METHODS:
            return True
        if obj.user == request.user:
            return True
        if contact_is_no_user_and_user_not_guest(obj, request):
            return True

        return False
