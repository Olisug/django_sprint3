from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PublishedCreatedModel(models.Model):
    """Абстрактная модель. Добавляет флаг is_published и crated_at."""
    is_published = models.BooleanField('Опубликовано', default=True,
                                       help_text='Снимите галочку, чтобы '
                                                 'скрыть публикацию.')
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True


class Category(PublishedCreatedModel):
    """Модель для определения категории"""
    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    slug = models.SlugField('Идентификатор', unique=True,
                            help_text='Идентификатор страницы для URL; '
                                      'разрешены символы латиницы, цифры, '
                                      'дефис и подчёркивание.')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedCreatedModel):
    """Модель для определения местоположения"""
    name = models.CharField('Название места', max_length=256)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(PublishedCreatedModel):
    """Основная модель,  определяющая перечень публикаций и основную
    информацию о них"""
    title = models.CharField('Заголовок', max_length=256)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата и время публикации',
                                    auto_now_add=False,
                                    help_text='Если установить дату и '
                                    'время в будущем — можно делать '
                                    'отложенные публикации.')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор публикации',
                               related_name='posts')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL,
                                 blank=True, null=True,
                                 verbose_name='Местоположение',
                                 related_name='posts')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='Категория',
                                 related_name='posts')

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title
