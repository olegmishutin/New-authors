from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250)
    is_author = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='profiles_photo', null=True, blank=True)
    short_description = models.CharField(max_length=450)

    class Meta:
        db_table = 'Profile'
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.full_name
