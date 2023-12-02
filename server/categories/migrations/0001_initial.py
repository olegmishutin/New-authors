# Generated by Django 4.2.7 on 2023-12-02 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.ImageField(upload_to='categories_icons')),
                ('name', models.CharField(max_length=250)),
                ('short_description', models.CharField(max_length=400)),
                ('books_number', models.BigIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'db_table': 'Category',
            },
        ),
    ]
