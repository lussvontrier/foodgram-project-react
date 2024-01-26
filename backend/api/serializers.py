from rest_framework import serializers

from api.base_serializers import Base64ImageField
from users.serializers import FoodgramUserSerializer
from recipes.models import (
    Tag, Ingredient, Recipe, FavoriteRecipe, ShoppingList, IngredientRecipe)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientRecipeWriteSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeReadSerializer(serializers.ModelSerializer):
    author = FoodgramUserSerializer()
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = IngredientRecipeReadSerializer(many=True,
                                                 source='ingredientrecipe')

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',
                  'text', 'author', 'tags', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        current_user = self.context.get('request').user
        return obj.favorited_by.filter(user=current_user).exists()

    def get_is_in_shopping_cart(self, obj):
        current_user = self.context.get('request').user
        return obj.added_to_shopping_list_by.filter(user=current_user).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get('image'):
            representation['image'] = instance.image.url
        return representation


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField(use_url=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    ingredients = IngredientRecipeWriteSerializer(many=True,
                                                  source='ingredientrecipe')

    class Meta:
        model = Recipe
        fields = ('name', 'image', 'cooking_time',
                  'text', 'tags', 'ingredients')

    def validate(self, data):
        required_fields = ('name', 'cooking_time', 'text',
                           'tags', 'ingredients')

        for field_name in required_fields:
            if field_name not in data:
                raise serializers.ValidationError(
                    f"'{field_name}' is required but missing.")
            elif data[field_name] in [None, '', []]:
                raise serializers.ValidationError(
                    f"'{field_name}' cannot be empty.")
        return data

    def validate_ingredients(self, value):
        ingredient_ids = [ingredient.get('id') for ingredient in value]
        existing_ingredient_ids = set(Ingredient.objects.values_list(
            'id', flat=True))
        invalid_ingredient_ids = set(ingredient_ids) - existing_ingredient_ids
        if len(set(ingredient_ids)) < len(ingredient_ids):
            raise serializers.ValidationError(
                'Duplicate ingredient IDs are not allowed.')
        if invalid_ingredient_ids:
            raise serializers.ValidationError(
                f'The following tags do not exist {invalid_ingredient_ids}')
        return value

    def validate_tags(self, tags):
        tag_ids = set(tags)
        existing_tag_ids = set(Tag.objects.values_list('id', flat=True))
        invalid_tag_ids = tag_ids - existing_tag_ids
        if tag_ids < tags:
            raise serializers.ValidationError('Cannot include duplicate tags.')
        if invalid_tag_ids:
            raise serializers.ValidationError(
                f'The following tags do not exist {invalid_tag_ids}')

    def validate_cooking_time(self, cooking_time):
        if cooking_time < 1:
            raise serializers.ValidationError(
                'Cooking time cannot be less than a minute.')

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        request = self.context.get('request')
        recipe = Recipe.objects.create(author=request.user, **validated_data)

        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id')
            amount = ingredient_data.get('id')

            ingredient = Ingredient.objects.get(id=ingredient_id)
            IngredientRecipe.objects.create(recipe=recipe,
                                            ingredient=ingredient,
                                            amount=amount)

        tags = Tag.objects.filter(id__in=tags_data)
        recipe.tags.set(tags)
        return recipe

    def update(self, recipe, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe.ingredients.clear()
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data.get('id')
            amount = ingredient_data.get('id')

            ingredient = Ingredient.objects.get(id=ingredient_id)
            IngredientRecipe.objects.create(recipe=recipe,
                                            ingredient=ingredient,
                                            amount=amount)
        tags = Tag.objects.filter(id__in=tags_data)
        recipe.tags.set(tags)
        return super().update(recipe, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        serializer = RecipeReadSerializer(instance,
                                          context={'request': request})
        return serializer.data


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe')

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
        model = ShoppingList
        fields = ('user', 'recipe')

    def validate(self, data):
        current_user = data.get('user')
        if current_user.favorites.filter(recipe=data.get('recipe')).exists():
            raise serializers.ValidationError(
                'This recipe is already in Shopping List.')
        return data

    def to_representation(self, instance):
        recipe = instance.recipe
        return RecipeSummarySerializer(recipe).data
