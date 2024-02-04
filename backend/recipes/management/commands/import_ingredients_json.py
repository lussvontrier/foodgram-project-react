import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """
    Import ingredients from a JSON file into the database.

    This management command is used to populate the database with ingredients
    by reading data from a JSON file. It should be called from the command line
    using the following format:

    python manage.py import_ingredients

    The JSON file containing ingredient data should be located at
    'recipes/data/ingredients.json'.
    The JSON file should have the following structure for each ingredient:
    {
        "name": "Ingredient Name",
        "measurement_unit": "Unit of Measurement"
    }
    Example JSON file content:
    [
        {
            "name": "Flour",
            "measurement_unit": "grams"
        },
        {
            "name": "Sugar",
            "measurement_unit": "grams"
        },
        ...
    ]
    Upon successful execution, this command will import the ingredients
    into the database and display a success message.
    """
    help = 'Import ingredients from a JSON file into the database'

    def handle(self, *args, **kwargs):
        hardcoded_path = 'recipes/data/ingredients.json'

        try:
            with open(hardcoded_path, 'r', encoding='utf-8') as file:
                ingredients_data = json.load(file)

            ingredients_to_create = [
                Ingredient(
                    name=ingredient_data['name'],
                    measurement_unit=ingredient_data['measurement_unit']
                )
                for ingredient_data in ingredients_data
            ]

            Ingredient.objects.bulk_create(ingredients_to_create)

            self.stdout.write(self.style.SUCCESS(
                'Successfully imported ingredients.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(
                f'Error importing ingredients: {str(e)}'))
