# Generated by Django 3.1 on 2020-08-12 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_auto_20200811_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='cost',
            field=models.IntegerField(default=0, verbose_name='Стоимость вопроса'),
        ),
    ]
