from colorfield.fields import ColorField
from django.conf import settings
from django.core.validators import (
    MaxValueValidator, MinValueValidator
)
from django.db import models


FIELD_MAX_LENGTH = 200
COLOR_FIELD_MAX_LENGTH = 7
AMOUNT_FIELD_DEFAULT = 1
MIN_VALUE_VALIDATOR = 1
MAX_VALUE_VALIDATOR = 32763


class Tag(models.Model):
    name = models.CharField(
        'Name',
        max_length=FIELD_MAX_LENGTH,
        unique=True
    )
    color = ColorField(
        'HEX Color',
        max_length=COLOR_FIELD_MAX_LENGTH,
        unique=True,
    )
    slug = models.SlugField(
        'Slug',
        max_length=FIELD_MAX_LENGTH,
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Name', max_length=FIELD_MAX_LENGTH)
    measurement_unit = models.CharField(
        'Measurement Unit',
        max_length=FIELD_MAX_LENGTH
    )

    class Meta:
        ordering = ('name', 'measurement_unit')
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_name_measurement_unit'
            )
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Author of the recipe'
    )
    name = models.CharField('Name', max_length=FIELD_MAX_LENGTH)
    text = models.TextField('Description')
    image = models.ImageField('Image', upload_to='recipes/images/')
    cooking_time = models.PositiveIntegerField(
        'Cooking Time',
        validators=[MinValueValidator(MIN_VALUE_VALIDATOR)]
    )
    pub_date = models.DateTimeField(
        verbose_name='Date of creation.',
        auto_now_add=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Tags'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='IngredientRecipe',
        verbose_name='Ingredients'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='ingredientrecipe'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='ingredientrecipe'
    )
    amount = models.PositiveSmallIntegerField(
        'Ingredient Amount',
        default=AMOUNT_FIELD_DEFAULT,
        validators=[
            MinValueValidator(MIN_VALUE_VALIDATOR),
            MaxValueValidator(MAX_VALUE_VALIDATOR)
        ],
    )

    def __str__(self):
        return (
            f'Recipe of {self.recipe} needs {self.ingredient}'
            f' in the amount of {self.amount}'
        )


class UserRecipeBaseModel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='User',
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        verbose_name='Recipe'
    )

    class Meta:
        abstract = True
        ordering = ('user', 'recipe')


class FavoriteRecipe(UserRecipeBaseModel):

    class Meta(UserRecipeBaseModel.Meta):
        verbose_name = 'Favorite Recipe'
        verbose_name_plural = 'Favorite Recipes'
        default_related_name = 'favoriterecipe'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_recipe_for_favoriterecipe'
            )
        ]

    def __str__(self):
        return (
            f'{self.recipe} favorited by {self.user}'
        )


class ShoppingCart(UserRecipeBaseModel):

    class Meta(UserRecipeBaseModel.Meta):
        verbose_name = 'Shopping Cart'
        verbose_name_plural = 'Shopping Carts'
        default_related_name = 'shoppingcart'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_recipe_for_shoppingcart'
            )
        ]

    def __str__(self):
        return (
            f'{self.recipe} added to shopping cart by {self.user}'
        )
