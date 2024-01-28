from rest_framework.permissions import IsAuthenticatedOrReadOnly


class IsAuthorOrAdminOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.user.is_admin
            or request.user.is_staff
        )
