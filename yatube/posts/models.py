from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Group model"""

    title = models.CharField('Имя', max_length=200)
    slug = models.SlugField('Адрес', max_length=9, unique=True)
    description = models.TextField('Описание')

    class Meta:
        verbose_name_plural = 'Сообщества'
        verbose_name = 'Сообщество'

    def __str__(self):
        return self.title


class Post(models.Model):
    """Post model"""

    text = models.TextField('Текст поста', help_text='Введите текст поста')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Сообщество',
        help_text='Сообщество, к которому будет относиться пост',
    )
    image = models.ImageField('Картинка', upload_to='posts/', blank=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name_plural = 'Публикации'
        verbose_name = 'Публикация'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Comments model"""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    text = models.TextField(
        'Текст комментария', help_text='Введите комментарий'
    )
    created = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'комментарии'
        verbose_name = 'комментарий'


class Follow(models.Model):
    """Follow user to author model"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='авторы',
    )
