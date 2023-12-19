# Generated by Django 5.0 on 2023-12-19 20:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_rename_creation_date_book_publication_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book', verbose_name='Книга'),
        ),
        migrations.AlterField(
            model_name='review',
            name='date_added',
            field=models.DateField(auto_now=True, verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
