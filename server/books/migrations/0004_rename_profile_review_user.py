# Generated by Django 4.2.7 on 2023-12-03 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_remove_book_author_profile_remove_book_date_added_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='profile',
            new_name='user',
        ),
    ]
