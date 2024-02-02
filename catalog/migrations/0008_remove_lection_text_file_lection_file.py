# Generated by Django 4.2.6 on 2023-11-02 12:05

import catalog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_lection'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lection',
            name='text_file',
        ),
        migrations.AddField(
            model_name='lection',
            name='file',
            field=models.FileField(blank=True, upload_to=catalog.models.get_upload_path),
        ),
    ]
