# Generated by Django 5.0 on 2024-01-08 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postcategory',
            old_name='category',
            new_name='categoryTrough',
        ),
        migrations.RenameField(
            model_name='postcategory',
            old_name='post',
            new_name='postTrough',
        ),
    ]