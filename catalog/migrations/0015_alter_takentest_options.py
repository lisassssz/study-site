# Generated by Django 4.2.6 on 2023-11-08 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_remove_answer_question_remove_answer_text_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='takentest',
            options={'permissions': (('can_watch', 'See tests results'),)},
        ),
    ]