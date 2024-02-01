import json
from django.core.management.base import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
    """
    Import tags from a JSON file into the database.

    This management command is used to populate the database with tags
    by reading data from a JSON file. It should be called from the command line
    using the following format:

    python manage.py import_tags

    The JSON file containing tag data should be located at
    'recipes/data/tags.json'.
    The JSON file should have the following structure for each tag:

    {
        "name": "Tag Name",
        "color": "Tag Color",
        "slug": "Tag Slug"
    }

    Example JSON file content:
    [
        {
            "name": "Dessert",
            "color": "#FF5733",
            "slug": "dessert"
        },
        {
            "name": "Breakfast",
            "color": "#E6DF44",
            "slug": "breakfast"
        },
        ...
    ]
    Upon successful execution, this command will import the tags into the
    database and display success messages for each tag created.
    """
    help = 'Import tags from tags.json'

    def handle(self, *args, **options):
        try:
            with open('recipes/data/tags.json', 'r') as file:
                tags = json.load(file)

            for tag_data in tags:
                name = tag_data.get('name')
                color = tag_data.get('color')
                slug = tag_data.get('slug')

                Tag.objects.get_or_create(name=name, color=color, slug=slug)
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully created tag: {name}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(
                'tags.json not found. Please create the file.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
