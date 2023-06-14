import csv

from django.core.management import BaseCommand
import os

from Foodgram.settings import BASE_DIR
from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        path = os.path.join(BASE_DIR, 'data/ingredients.csv')
        with open(path ,
                  encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            # Ingredient.objects.all().delete()
            count = 0
            for row in csv_reader:
                check_empty = Ingredient.objects.filter(
                    name=row['name'], measurement_unit=row['measurement_unit']).exists()
                if not check_empty:
                    new_obj = Ingredient.objects.create(
                        name=row['name'], measurement_unit=row['measurement_unit'])
                    count += 1
            print(f'Загрузка завершена! Добавлено записей - {count}.')
