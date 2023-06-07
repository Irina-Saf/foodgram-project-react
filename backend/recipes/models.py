from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        help_text='Введите название тега',
        blank=True,
        unique=True
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет',
        unique=True
    )

    slug = models.SlugField(
        max_length=200,
        verbose_name='Слаг',
        unique=True
    )

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
        blank=True
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/image/',
        blank=True
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Введите описание рецепта',
        blank=True
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        help_text='Введите время приготовлления',
        blank=True
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
        blank=True
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
    amount = models.IntegerField(
        'Количество',
        validators=[MinValueValidator(1)]
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
