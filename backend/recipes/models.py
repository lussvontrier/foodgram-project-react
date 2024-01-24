from django.db import models
from django.core.validators import RegexValidator

FIELD_MAX_LENGTH = 200
COLOR_FIELD_MAX_LENGTH = 7


class Tag(models.Model):
    name = models.CharField('Name', max_length=FIELD_MAX_LENGTH)
    color = models.CharField('HEX Color', max_length=COLOR_FIELD_MAX_LENGTH)
    slug = models.SlugField(
        'Slug',
        max_length=FIELD_MAX_LENGTH,
        unique=True,
        validators=[RegexValidator(regex='^[-a-zA-Z0-9_]+$')]
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Name', max_length=FIELD_MAX_LENGTH)
    measurement_unit = models.CharField('Measurement Unit',
                                        max_length=FIELD_MAX_LENGTH)

    def __str__(self):
        return self.name
