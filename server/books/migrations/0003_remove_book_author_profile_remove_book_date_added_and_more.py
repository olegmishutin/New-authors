# Generated by Django 4.2.7 on 2023-12-02 20:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0002_alter_category_books_number_alter_category_icon_and_more'),
        ('books', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author_profile',
        ),
        migrations.RemoveField(
            model_name='book',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='book',
            name='image',
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.ImageField(default='', upload_to='books_images', verbose_name='Обложка'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='creation_date',
            field=models.DateField(auto_now=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='book',
            name='categories',
            field=models.ManyToManyField(db_table='BookCategories', to='categories.category', verbose_name='Категории'),
        ),
        migrations.AlterField(
            model_name='book',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='book',
            name='file',
            field=models.FileField(upload_to='books_files', verbose_name='Файл'),
        ),
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(max_length=250, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='book',
            name='pages_number',
            field=models.IntegerField(verbose_name='Количесвто страниц'),
        ),
    ]
