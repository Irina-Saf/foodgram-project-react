from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import PositiveSmallIntegerField

from users.models import User

MIN_VALUE_COOKING_TIME = 1,
MAX_VALUE_COOKING_TIME = 300,
MIN_VALUE_AMOUNT = 1,


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        help_text='Введите название тега',
        unique=True
    )
    color = ColorField(
        format="hexa",
        verbose_name='Цвет',
        unique=True
    )

    slug = models.SlugField(
        max_length=200,
        verbose_name='Слаг',
        unique=True
    )

    def trim10(self):
        return u"%s..." % (self.slug[:10],)
    trim10.short_description = 'Слаг'

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        """Строковое представление модели."""
        return self.slug


class Ingredient(models.Model):
    """Модель ингредиентов"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
    )

    def trim30(self):
        return u"%s..." % (self.name[:30],)
    trim30.short_description = 'Название ингредиента'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/image/',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Введите описание рецепта',
    )
    cooking_time = PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Введите время приготовлления',
        default=0,
        validators=(
            MinValueValidator(*MIN_VALUE_COOKING_TIME),
            MaxValueValidator(*MAX_VALUE_COOKING_TIME),
        ),
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='recipes',
        help_text='Выберите автора рецепта',
        # null=True
    )

    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        related_name='recipes',
        help_text='Укажите тег рецепта',
        verbose_name='Тег рецепта'
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        related_name='recipes',
        help_text='Укажите ингредиент рецепта',
        verbose_name='Ингредиент рецепта'
    )

    def trim50(self):
        return u"%s..." % (self.name[:50],)
    trim50.short_description = 'Название рецепта'

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    """Модель тегов рецептов"""
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Теги',
        help_text='Укажите теги рецепта'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Укажите рецепт')

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецепта'
        constraints = [
            models.UniqueConstraint(fields=['tag', 'recipe'],
                                    name='unique_tag_recipe')
        ]

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class IngredientRecipe(models.Model):
    """Модель ингредиентов для рецепта"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Ингредиент'
    )
    amount = PositiveSmallIntegerField(
        'Количество',
        validators=[MinValueValidator(*MIN_VALUE_AMOUNT)]
    )

    class Meta:
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_combination'
            )
        ]

    def str(self):
        return (f'{self.recipe.name}: '
                f'{self.ingredient.name} - '
                f'{self.amount} '
                f'{self.ingredient.measurement_unit}')


class Basket(models.Model):
    """Модель корзины"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Укажите пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='bascets',
        verbose_name='Рецепты',
        help_text='Выберите рецепт'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_basket')
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class Favorite(models.Model):
    """Избранные рецепты."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Укажите пользователя'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
        help_text='Укажите рецепт'
    )

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite')
        ]

    def __str__(self):
        return f'{self.recipe} {self.user}'
