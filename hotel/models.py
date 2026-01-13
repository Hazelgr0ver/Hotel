from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class PublishedModel(models.Model):
    is_published = models.BooleanField('Опубликовано', default=True,
                                       help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True


class Category(PublishedModel):
    title = models.CharField('Название категории', max_length=256)
    description = models.TextField('Описание')
    slug = models.SlugField(unique=True, verbose_name='Идентификатор',
                            help_text='Идентификатор страницы для URL; '
                                      'разрешены символы латиницы, цифры, дефис и подчёркивание.')
    image = models.ImageField('Фото', upload_to='categories/', blank=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField('Название места', max_length=256)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Room(PublishedModel):
    title = models.CharField('Название номера', max_length=256)
    text = models.TextField('Описание')
    slug = models.SlugField('Идентификатор', unique=True,
                            help_text='Идентификатор страницы для URL; '
                                      'разрешены символы латиницы, цифры, дефис и подчёркивание.')
    image = models.ImageField('Фото', upload_to='rooms/', blank=True)
    pub_date = models.DateTimeField('Дата и время публикации',
                                    help_text='Если установить дату и время в будущем — '
                                              'можно делать отложенные публикации.')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Местоположение')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Категория')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField('Вместимость')

    class Meta:
        verbose_name = 'номер'
        verbose_name_plural = 'Номера'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings',
                             verbose_name='Номер')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор бронирования')
    check_in = models.DateField('Дата заезда')
    check_out = models.DateField('Дата выезда')
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'бронирование'
        verbose_name_plural = 'Бронирования'

    def __str__(self):
        return f'Бронирование {self.room} от {self.author}'


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='comments',
                             verbose_name='Номер')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return f'Комментарий от {self.author} к {self.room}'
