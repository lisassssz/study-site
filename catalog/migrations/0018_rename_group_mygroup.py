# Generated by Django 4.2.6 on 2023-11-11 09:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0017_group'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Group',
            new_name='MyGroup',
        ),
    ]
