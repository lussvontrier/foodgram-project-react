from django.contrib import admin
from .models import (Tag, Ingredient, Recipe,
                     FavoriteRecipe, ShoppingList)


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


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')


@admin.register(Recipe)
class RecipeListAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorites_count')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name', 'author__username')

    def favorites_count(self, obj):
        return obj.favorited_by.all().count()

    favorites_count.short_description = 'Favorites Count'
