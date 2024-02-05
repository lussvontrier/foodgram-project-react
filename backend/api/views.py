from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import ApiPageNumberPagination
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (
    FavoriteSerializer, FoodgramUserSerializer, IngredientSerializer,
    RecipeReadSerializer, RecipeWriteSerializer, ShoppingCartSerializer,
    SubscriptionSerializer, TagSerializer, SubscribeUnsubscribeSerializer
)
from recipes.models import (
    Recipe, Tag, Ingredient, FavoriteRecipe, ShoppingCart, IngredientRecipe
)
from users.models import FoodgramUser, Subscription


class FoodgramUserViewSet(UserViewSet):
    queryset = FoodgramUser.objects.all()
    serializer_class = FoodgramUserSerializer
    pagination_class = ApiPageNumberPagination

    def get_permissions(self):
        if self.action == 'me':
            return (IsAuthenticated(),)

        return super().get_permissions()

    @action(detail=True, methods=('post',),
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id):
        data = {
            'subscriber': request.user.id,
            'subscribed_to': id
        }
        serializer = SubscribeUnsubscribeSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        subscription_target = get_object_or_404(FoodgramUser, pk=id)
        response_serializer = SubscriptionSerializer(
            subscription_target, context={'request': request}
        )
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED
        )

    @subscribe.mapping.delete
    def unsubscribe(self, request, id):
        subscriber = request.user
        subscription_target = get_object_or_404(FoodgramUser, pk=id)
        deleted, _ = Subscription.objects.filter(
            subscriber=subscriber, subscribed_to=subscription_target
        ).delete()

        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise ValidationError({'error': 'Subscription does not exist'})

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        current_user = request.user
        subscriptions = FoodgramUser.objects.filter(
            subscribers__subscriber=current_user)
        page = self.paginate_queryset(subscriptions)
        serializer = SubscriptionSerializer(page,
                                            many=True,
                                            context={'request': request})
        return self.get_paginated_response(serializer.data)


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
    permission_classes = IsAuthorOrAdminOrReadOnly

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return super().get_serializer_class()
        return RecipeReadSerializer

    @staticmethod
    def generate_shopping_cart_content(shopping_cart_content):
        response = HttpResponse(content_type='text/plain')

        for item in shopping_cart_content:
            ingredient_name = item['ingredient__name']
            measurement_unit = item['ingredient__measurement_unit']
            amount = item['amount']

            response.write(
                f'{ingredient_name} ({measurement_unit}) — {amount}\n'
            )

        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"'
        )
        return response

    @action(detail=False, methods=('get',),
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        shopping_cart_content = (
            IngredientRecipe.objects
            .filter(recipe__shoppingcart__user=request.user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(amount=Sum('amount'))
            .order_by('ingredient__name')
        )

        return self.generate_shopping_cart_content(shopping_cart_content)

    def base_create_action(self, request, pk, serializer_class):
        data = {
            'user': request.user.id,
            'recipe': pk
        }
        serializer = serializer_class(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def base_delete_action(self, request, pk, model_class):
        recipe = get_object_or_404(Recipe, id=pk)

        deleted, _ = model_class.objects.filter(
            user=request.user, recipe=recipe
        ).delete()

        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise ValidationError({'error': 'This recipe was not found.'})

    @action(detail=True, methods=('post',),
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        return self.base_create_action(request, pk, FavoriteSerializer)

    @favorite.mapping.delete
    def unfavorite(self, request, pk):
        return self.base_delete_action(request, pk, FavoriteRecipe)

    @action(detail=True, methods=('post',),
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        return self.base_create_action(request, pk, ShoppingCartSerializer)

    @shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk):
        return self.base_delete_action(request, pk, ShoppingCart)
