# Generated by Django 4.2.7 on 2023-11-28 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('user_profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('image', models.ImageField(upload_to='books_images')),
                ('pages_number', models.IntegerField()),
                ('description', models.TextField()),
                ('date_added', models.DateField(auto_now=True)),
                ('file', models.FileField(upload_to='books_files')),
                ('author_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profiles.profile')),
                ('categories', models.ManyToManyField(db_table='BookCategories', to='categories.category')),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
                'db_table': 'Book',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('rating', models.FloatField()),
                ('date_added', models.DateField(auto_now=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profiles.profile')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'db_table': 'Review',
            },
        ),
    ]
