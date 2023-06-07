import csv

from django.core.management import BaseCommand

from Foodgram.settings import BASE_DIR
from recipes.models import Ingredient

# CSV_FILES_DIR = 'C:\\Users\\lis91\\Documents\\Dev\\foodgram-project-react\\data/'

DIR = str(BASE_DIR).replace('backend', 'data\\')


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(DIR + 'ingredients.csv',
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
