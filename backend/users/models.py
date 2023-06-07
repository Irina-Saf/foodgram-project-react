from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        db_index=True,
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        help_text='Введите логин'
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
        help_text='Введите имя'
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True,
        help_text='Введите фамилию'

    )
    email = models.EmailField(
        db_index=True,
        verbose_name='Email пользователя',
        max_length=254,
        unique=True,
        help_text='Введите email'

    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
        help_text='Введите пароль'
    )

    class Meta:
        """Каждый логин может быть привязан к определенному email."""
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            )
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Строковое представление модели."""
        return self.username


class Subscribe(models.Model):
    """Модели подписчиков."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
        help_text='Укажите юзера, кто совершает подписку'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='Укажите автора, на которого подписываются'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name='unique_subscribe')
        ]

    def __str__(self):
        return f'{self.user} {self.following}'
