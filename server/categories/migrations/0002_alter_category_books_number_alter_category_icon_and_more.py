# Generated by Django 4.2.7 on 2023-12-02 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='books_number',
            field=models.BigIntegerField(default=0, verbose_name='Количество книг'),
        ),
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=models.ImageField(upload_to='categories_icons', verbose_name='Иконка'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='category',
            name='short_description',
            field=models.CharField(max_length=400, verbose_name='Краткое описание'),
        ),
    ]
