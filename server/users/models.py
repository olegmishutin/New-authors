import os
from django.db import models
from django.db.models import Avg, Count
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = None
    last_name = None

    full_name = models.CharField(max_length=250, verbose_name='Полное имя (ФИО)')
    is_author = models.BooleanField(default=False, verbose_name='Является автором')
    photo = models.ImageField(upload_to='profiles_photo', verbose_name='Фото', null=True, blank=True)
    short_description = models.CharField(max_length=450, verbose_name='Краткое описание')

    REQUIRED_FIELDS = ['email', 'full_name']

    class Meta:
        db_table = 'User'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def getAllWithStatistics(self):
        return self.objects.filter(is_author=True).annotate(rating=Avg('book__review__rating'),
                                                            reviewsCount=Count('book__review'))

    def getRating(self):
        return self.book_set.all().aggregate(rating=Avg('review__rating', default=0)).get('rating')

    def getReviewsCount(self):
        return self.book_set.all().aggregate(reviewsCount=Count('review')).get('reviewsCount')

    def setPhoto(self, photo):
        if photo:
            if os.path.isfile(self.photo.path):
                os.remove(self.photo.path)
            self.photo = photo

    def setFullName(self, fullName):
        if fullName:
            self.full_name = fullName

    def get_full_name(self):
        return self.full_name

    def delete(self, using=None, keep_parents=False):
        if os.path.isfile(self.photo.path):
            os.remove(self.photo.path)
        return super(User, self).delete()
