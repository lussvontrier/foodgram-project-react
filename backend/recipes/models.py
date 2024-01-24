from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

FIELD_MAX_LENGTH = 200
COLOR_FIELD_MAX_LENGTH = 7


class Tag(models.Model):
    name = models.CharField('Name',
                            max_length=FIELD_MAX_LENGTH,
                            unique=True)
    color = models.CharField(
        'HEX Color',
        max_length=COLOR_FIELD_MAX_LENGTH,
        unique=True,
        validators=[
            RegexValidator(
                regex='^#(?:[0-9a-fA-F]{3}){1,2}$',
                message='Enter a valid HEX color',
            ),
            ],
    )
    slug = models.SlugField(
        'Slug',
        max_length=FIELD_MAX_LENGTH,
        unique=True,
        validators=[RegexValidator(regex='^[-a-zA-Z0-9_]+$')]
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Name', max_length=FIELD_MAX_LENGTH)
    measurement_unit = models.CharField('Measurement Unit',
                                        max_length=FIELD_MAX_LENGTH)

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

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
    cooking_time = models.PositiveIntegerField('Cooking Time')
    pub_date = models.DateTimeField(
        verbose_name='Date of creation.',
        auto_now_add=True
    )
    tags = models.ManyToManyField(Tag,
                                  related_name='recipes',
                                  verbose_name='Tags')
    ingredients = models.ManyToManyField(Ingredient,
                                         related_name='recipes',
                                         through='IngredientRecipe',
                                         verbose_name='Ingredients')

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField('Ingredient Amount', default=1)

    def __str__(self):
        return (
            f'Recipe of {self.recipe} needs {self.ingredient}'
            f' in the amount of {self.amount}'
        )
