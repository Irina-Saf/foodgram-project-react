# Описание
Проект "Foodgram" – это "продуктовый помощник". На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

# Запуск проекта локально:
Клонировать репозиторий:
git@github.com:Irina-Saf/foodgram-project-react.git

Перейти в него в командной строке
сd foodgram-project-react

Создать виртуальное окружение:
python3 -m venv venv

Активировать виртуальное окружение:
source venv/bin/activate (Linux/macOS)
source venv/Scripts/activate (Windows)

Установить зависимости из файла requirements:
pip install -r requirements.txt

Выполнить миграции:
python3 manage.py migrate

Запустить проект:
python3 manage.py runserver

# В API доступны одни из следующих эндпоинтов:
[GET - запрос] /api/v1/users/ - Получить список всех пользователей.
[POST - запрос] /api/v1/users/ - Добавление пользователя.
[GET - запрос] /api/v1/tags/ - Получить список всех тегов.
[POST - запрос] /api/v1/recipes/ - Добавление рецепта.
[GET - запрос] /api/v1/recipes/download_shopping_cart/ - Скачать файл со списком покупок.
[POST - запрос] /api/v1/recipes/{id}/favorite/ - Добавить рецепт в избранное.
[GET - запрос] /api/v1/ingredients/ - Получить список ингредиентов.

# Работа с Docker-контейнерами:
	Образы irinasaf/foodgram_frontend и irinasaf/ foodgram_backend находятся на DockerHub;
	Проект был развернут на сервере: http://http://158.160.28.88/admin
# Развертывание проекта
1. Установить на сервере docker и docker-compose
2. Создайте файл .env в дирректории /infra
3. Выполнить команду docker-compose up -d --buld.
4. Применить миграции:
    docker-compose exec backend python manage.py makemigrations
    docker-compose exec backend python manage.py migrate.
5. Создать суперюзера:
    docker-compose exec backend python manage.py createsuperuser.
6. Соберanm статику:
    docker-compose exec backend python manage.py collectstatic --no-input.
7. Наполнить базу ингредиентами docker-compose exec backend python manage.py load_csv.

# Автор проекта
Ирина Сафронова
