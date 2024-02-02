# Generated by Django 4.2.6 on 2023-11-06 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_remove_answer_answer_text_remove_question_answers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='question',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='text',
        ),
        migrations.RemoveField(
            model_name='question',
            name='test',
        ),
        migrations.RemoveField(
            model_name='question',
            name='text',
        ),
        migrations.AddField(
            model_name='answer',
            name='answer_text',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='answers',
            field=models.ManyToManyField(to='catalog.answer'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_text',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='questions',
            field=models.ManyToManyField(to='catalog.question'),
        ),
        migrations.AlterField(
            model_name='test',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.section'),
        ),
        migrations.AlterField(
            model_name='test',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]