
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.filters import SearchFilter

from recipes.models import Tag, Ingredient, Recipe
from api.serializers import TagSerializer, IngredientSerializer
from api.pagination import ApiPageNumberPagination


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = ApiPageNumberPagination