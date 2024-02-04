from django.db import transaction
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator

from api.base_fields import Base64ImageField
from recipes.models import (
    Tag, Ingredient, Recipe, FavoriteRecipe, ShoppingCart, IngredientRecipe
)
from users.models import FoodgramUser, Subscription


class FoodgramUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = FoodgramUser
        fields = ('username', 'email', 'id', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and obj.subscribers.filter(
                subscriber=request.user).exists()
        )


class SubscriptionSerializer(FoodgramUserSerializer):
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta(FoodgramUserSerializer.Meta):
        model = FoodgramUser
        fields = FoodgramUserSerializer.Meta.fields + ('recipes',
                                                       'recipes_count',)

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        recipes = obj.recipes.all()

        if recipes_limit and recipes_limit.isdigit():
            recipes = recipes[:int(recipes_limit)]

        serializer = RecipeSummarySerializer(recipes, many=True)
        return serializer.data


class SubscribeUnsubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('subscriber', 'subscribed_to')

    def validate(self, data):
        subscriber = data.get('subscriber')
        subscription_target = data.get('subscribed_to')

        if subscriber == subscription_target:
            raise serializers.ValidationError(
                {'error': 'Cannot subscribe to yourself'}
            )

        if Subscription.objects.filter(
                subscriber=subscriber,
                subscribed_to=subscription_target).exists():
            raise serializers.ValidationError(
                {'error': 'Subscription already exists'}
            )

        return data


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
    image = serializers.SerializerMethodField(
        'get_image',
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',
                  'text', 'author', 'tags', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart')

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and obj.favoriterecipe.filter(user=request.user).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (
            request
            and request.user.is_authenticated
            and obj.shoppingcart.filter(user=request.user).exists()
        )


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
                           'tags', 'ingredientrecipe')

        for field_name in required_fields:
            if field_name not in data:
                raise serializers.ValidationError(
                    f"'{field_name}' is required but missing.")
            elif data[field_name] in [None, '', []]:
                raise serializers.ValidationError(
                    f"'{field_name}' cannot be empty.")
        return data

    def validate_ingredients(self, ingredients):
        existing_ingredients = Ingredient.objects.all()
        ingredient_objects = []

        ingredient_names = [ingredient['id'] for ingredient in ingredients]
        if len(ingredient_names) != len(set(ingredient_names)):
            raise serializers.ValidationError(
                'Duplicate ingredients are not allowed.')

        for ingredient_data in ingredients:
            ingredient_name = ingredient_data.get('id', None)
            amount = ingredient_data.get('amount', None)
            try:
                ingredient_obj = existing_ingredients.get(name=ingredient_name)
            except Ingredient.DoesNotExist:
                raise serializers.ValidationError(
                    f'Ingredient with name "{ingredient_name}" does not exist')

            ingredient_objects.append({'id': ingredient_obj, 'amount': amount})

        return ingredients

    def validate_tags(self, tags):
        existing_tags = Tag.objects.all()
        tag_names = [tag.name for tag in tags]

        if len(tag_names) != len(set(tag_names)):
            raise serializers.ValidationError('Cannot include duplicate tags.')

        invalid_tags = [tag for tag in tags if tag not in existing_tags]
        if invalid_tags:
            invalid_tag_names = [tag.name for tag in invalid_tags]
            raise serializers.ValidationError(
                f'The following tags do not exist:'
                f'{", ".join(invalid_tag_names)}')

        return tags

    def process_ingredients(self, recipe, ingredients_data):
        for ingredient_data in ingredients_data:
            ingredient = ingredient_data.get('id')
            amount = ingredient_data.get('amount')

            IngredientRecipe.objects.create(recipe=recipe,
                                            ingredient=ingredient,
                                            amount=amount)

    @transaction.atomic
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredientrecipe')
        tags = validated_data.pop('tags')
        request = self.context.get('request')
        recipe = Recipe.objects.create(author=request.user, **validated_data)

        self.process_ingredients(recipe, ingredients_data)
        recipe.tags.set(tags)
        return recipe

    @transaction.atomic
    def update(self, recipe, validated_data):
        ingredients_data = validated_data.pop('ingredientrecipe')
        tags = validated_data.pop('tags')
        recipe.ingredients.clear()

        self.process_ingredients(recipe, ingredients_data)
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
        validators = [
            UniqueTogetherValidator(
                queryset=FavoriteRecipe.objects.all(),
                fields=('user', 'recipe'),
                message='This recipe is already in Favorites.'
            )
        ]

    def to_representation(self, instance):
        recipe = instance.recipe
        return RecipeSummarySerializer(recipe).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='This recipe is already in Shopping Cart.'
            )
        ]

    def to_representation(self, instance):
        recipe = instance.recipe
        return RecipeSummarySerializer(recipe).data
