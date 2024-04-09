import os
from django.db import models
from django.db.models import Avg, Count
from django.contrib.auth.models import AbstractUser
from New_authors.helpers.functions import changeFile


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

    @classmethod
    def getAuthors(cls, **kwargs):
        return cls.objects.filter(is_author=True, **kwargs).annotate(rating=Avg('book__review__rating', default=0),
                                                                     reviewsCount=Count('book__review'))

    def getRating(self):
        booksRatingSum = 0
        booksWithRating = self.book_set.all().annotate(rating=Avg('review__rating', default=0))

        for book in booksWithRating:
            booksRatingSum += book.rating
        return round(booksRatingSum / len(booksWithRating), 1) if len(booksWithRating) > 0 else 0

    def getReviewsCount(self):
        return self.book_set.all().aggregate(reviewsCount=Count('review')).get('reviewsCount')

    def setPhoto(self, photo):
        self.photo = changeFile(self.photo, photo)

    def setFullName(self, fullName):
        if fullName:
            self.full_name = fullName

    def get_full_name(self):
        return self.full_name

    def delete(self, using=None, keep_parents=False):
        changeFile(self.photo, deleteOnly=True)

        for book in self.book_set.all():
            book.delete()
        return super(User, self).delete()
