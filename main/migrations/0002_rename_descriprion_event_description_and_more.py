# Generated by Django 5.1.1 on 2024-09-29 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='descriprion',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='place',
            old_name='descriprion',
            new_name='description',
        ),
    ]
