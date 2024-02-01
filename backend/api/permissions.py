from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        BasePermission)


class IsAuthorOrAdminOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.user.is_staff
        )


class AllowAnyExceptMe(BasePermission):
    def has_permission(self, request, view):
        if '/users/me/' in request.path and not request.user.is_authenticated:
            return False
        return True
