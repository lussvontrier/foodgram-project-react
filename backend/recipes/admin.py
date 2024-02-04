from django.contrib import admin

from .models import (
    Tag, Ingredient, Recipe,
    FavoriteRecipe, ShoppingCart, IngredientRecipe)


class IngredientInline(admin.TabularInline):
    model = IngredientRecipe


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(FavoriteRecipe)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')


@admin.register(Recipe)
class RecipeListAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorites_count')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name', 'author__username')
    inlines = (IngredientInline,)

    @admin.display(description='Favorites Count')
    def favorites_count(self, obj):
        return obj.favoriterecipe.all().count()
