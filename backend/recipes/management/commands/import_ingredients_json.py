import json
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Import ingredients from a JSON file into the database'

    def handle(self, *args, **kwargs):
        hardcoded_path = 'recipes/data/ingredients.json'

        try:
            with open(hardcoded_path, 'r', encoding='utf-8') as file:
                ingredients_data = json.load(file)

            for ingredient_data in ingredients_data:
                Ingredient.objects.create(
                    name=ingredient_data['name'],
                    measurement_unit=ingredient_data['measurement_unit']
                )

            self.stdout.write(self.style.SUCCESS(
                'Successfully imported ingredients.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(
                f'Error importing ingredients: {str(e)}'))
