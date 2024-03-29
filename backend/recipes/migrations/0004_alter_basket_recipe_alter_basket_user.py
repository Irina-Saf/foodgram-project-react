# Generated by Django 4.2.1 on 2023-06-16 19:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0003_alter_tag_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basket',
            name='recipe',
            field=models.ForeignKey(
                help_text='Выберите рецепт',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='baskets',
                to='recipes.recipe',
                verbose_name='Рецепты'),
        ),
        migrations.AlterField(
            model_name='basket',
            name='user',
            field=models.ForeignKey(
                help_text='Укажите пользователя',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='baskets',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Пользователь'),
        ),
    ]
