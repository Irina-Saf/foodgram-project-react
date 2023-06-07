from django.contrib import admin

from users.models import Subscribe, User

from .models import (Basket, Favorite, Ingredient, IngredientRecipe, Recipe,
                     Tag, TagRecipe)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'password'
    )
    search_fields = ('username',)
    empty_value_display = "-пусто-"


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'following'
    )
    search_fields = ('user',)
    empty_value_display = "-пусто-"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    search_fields = ('name',)
    empty_value_display = "-пусто-"
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)
    empty_value_display = "-пусто-"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'text',
        'cooking_time',
        'pub_date',
        'author',
        # 'tags',
        # 'ingredients'
    )
    search_fields = ('name',)
    empty_value_display = "-пусто-"
    filter_horizontal = ('tags',)


@admin.register(TagRecipe)
class TagRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'tag',
        'recipe'
    )
    search_fields = ('tag',)
    empty_value_display = "-пусто-"


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'ingredient',
        'recipe',
        'amount'
    )
    search_fields = ('recipe',)
    empty_value_display = "-пусто-"


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )
    search_fields = ('user',)
    empty_value_display = "-пусто-"


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe'
    )
    search_fields = ('user',)
    empty_value_display = "-пусто-"
