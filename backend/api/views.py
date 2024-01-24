
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter

from recipes.models import Tag, Ingredient
from api.serializers import TagSerializer, IngredientSerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
