
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)

from django_filters.rest_framework import DjangoFilterBackend
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404

from recipes.models import (Tag, Ingredient, Recipe,
                            FavoriteRecipe, ShoppingList)
from api.pagination import ApiPageNumberPagination
from api.filters import RecipeFilter, IngredientFilter
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (
    TagSerializer, IngredientSerializer,
    RecipeReadSerializer, RecipeWriteSerializer,
    FavoriteSerializer, ShoppingListSerializer)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = ApiPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    serializer_class = RecipeWriteSerializer

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return super().get_serializer_class()
        return RecipeReadSerializer

    def get_permissions(self):
        if self.request.method in ('DELETE', 'PATCH'):
            return (IsAuthorOrAdminOrReadOnly(),)

        return (IsAuthenticatedOrReadOnly(),)

    @action(detail=False, methods=('get',),
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        shopping_list_items = ShoppingList.objects.filter(user=request.user)

        shopping_cart_content = {}

        for item in shopping_list_items:
            recipe = item.recipe
            recipe_ingredients = recipe.ingredientrecipe.all()

            for ingredient_recipe in recipe_ingredients:
                ingredient = ingredient_recipe.ingredient
                amount = ingredient_recipe.amount
                ingredient_name = ingredient.name
                measurement_unit = ingredient.measurement_unit

                if ingredient_name in shopping_cart_content:
                    shopping_cart_content[ingredient_name]['amount'] += amount
                else:
                    shopping_cart_content[ingredient_name] = {
                        'unit': measurement_unit,
                        'amount': amount
                    }

        response = HttpResponse(content_type='text/plain')
        for ingredient, info in shopping_cart_content.items():
            response.write(
                f"{ingredient} ({info['unit']}) — {info['amount']}\n")

        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"')
        return response

    @action(detail=True, methods=('post',),
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        data = {
            'user': request.user.id,
            'recipe': pk
        }
        serializer = FavoriteSerializer(data=data,
                                        context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def unfavorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        current_user = request.user
        data = {
            'user': request.user.id,
            'recipe': pk
        }
        serializer = FavoriteSerializer(data=data,
                                        context={'request': request})
        serializer.is_valid(raise_exception=True)

        FavoriteRecipe.objects.get(user=current_user, recipe=recipe).delete()
        return Response({'detail': 'Recipe removed from Favorites.'},
                        status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=('post',),
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        data = {
            'user': request.user.id,
            'recipe': pk
        }
        serializer = ShoppingListSerializer(data=data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        data = {
            'user': request.user.id,
            'recipe': pk
        }
        serializer = ShoppingListSerializer(data=data,
                                            context={'request': request})
        serializer.is_valid(raise_exception=True)

        current_user = request.user
        ShoppingList.objects.get(user=current_user, recipe=recipe).delete()
        return Response({'detail': 'Recipe removed from Shopping Cart.'},
                        status=status.HTTP_204_NO_CONTENT)
