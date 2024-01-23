from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.fields import SerializerMethodField

from users.models import FoodgramUser


class FoodgramUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = FoodgramUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class FoodgramUserSerializer(UserSerializer):

    class Meta:
        model = FoodgramUser
        fields = ('username', 'email', 'id', 'first_name', 'last_name',
                  'is_subscribed')

