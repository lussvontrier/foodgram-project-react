import json
from django.core.management.base import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
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
