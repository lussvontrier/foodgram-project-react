from djoser.views import UserViewSet

from users.models import FoodgramUser
from users.serializers import FoodgramUserSerializer
from users.pagination import CustomPageNumberPagination


class FoodgramUserViewSet(UserViewSet):
    queryset = FoodgramUser.objects.all()
    serializer_class = FoodgramUserSerializer
    pagination_class = CustomPageNumberPagination