from rest_framework import serializers

from recipes.models import (
    Tag, Ingredient, Recipe, FavoriteRecipe, ShoppingList)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('user', 'recipe')
        model = FavoriteRecipe

    def validate(self, data):
        current_user = data.get('user')
        if current_user.favorites.filter(recipe=data.get('recipe')).exists():
            raise serializers.ValidationError(
                'This recipe is already in Favorites.')
        return data

    def to_representation(self, instance):
        recipe = instance.recipe
        return RecipeSummarySerializer(recipe).data


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('user', 'recipe')
        model = ShoppingList

    def validate(self, data):
        current_user = data.get('user')
        if current_user.favorites.filter(recipe=data.get('recipe')).exists():
            raise serializers.ValidationError(
                'This recipe is already in Shopping List.')
        return data

    def to_representation(self, instance):
        recipe = instance.recipe
        return RecipeSummarySerializer(recipe).data
