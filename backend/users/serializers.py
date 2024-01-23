from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from users.models import FoodgramUser


class FoodgramUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = FoodgramUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password')


class FoodgramUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = FoodgramUser
        fields = ('username', 'email', 'id', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        current_user = self.context.get('request').user
        user_to_check = obj
        return user_to_check.subscribers.filter(
            subscriber=current_user).exists()


class SubscriptionSerializer(FoodgramUserSerializer):
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta(FoodgramUserSerializer.Meta):
        fields = FoodgramUserSerializer.Meta.fields + ('recipes',
                                                       'recipes_count',)

    # or change to get it with annotate
    def get_recipes_count(self, obj):
        pass

    def get_recipes(self, obj):
        pass