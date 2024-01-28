import django_filters

from recipes.models import Recipe, Tag


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(
        field_name='author__id',
    )

    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = django_filters.NumberFilter(method='filter_is_favorited')
    is_in_shopping_cart = django_filters.NumberFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = fields = ('tags', 'author', 'is_favorited',
                           'is_in_shopping_cart')

    def filter_favorited_by(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value == 1:
            return queryset.filter(favorited_by__user=user)
        elif user.is_authenticated and value == 0:
            return queryset.exclude(favorited_by__user=user)
        return queryset

    def filter_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value == 1:
            return queryset.filter(added_to_shopping_list_by__user=user)
        elif user.is_authenticated and value == 0:
            return queryset.exclude(added_to_shopping_list_by__user=user)
        return queryset
