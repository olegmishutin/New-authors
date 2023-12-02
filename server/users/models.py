from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = None
    last_name = None

    full_name = models.CharField(max_length=250)
    is_author = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='profiles_photo', null=True, blank=True)
    short_description = models.CharField(max_length=450)

    class Meta:
        db_table = 'User'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self):
        return self.full_name
