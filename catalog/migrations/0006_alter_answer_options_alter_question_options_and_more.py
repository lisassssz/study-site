# Generated by Django 4.2.6 on 2023-10-30 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_remove_test_subject_section_test_section'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'permissions': (('can_answer', 'Work with answer'),)},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'permissions': (('can_question', 'Work with question'),)},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'permissions': (('can__section', 'Work with section'),)},
        ),
        migrations.AlterModelOptions(
            name='test',
            options={'permissions': (('can_test', 'Work with test'),)},
        ),
    ]
