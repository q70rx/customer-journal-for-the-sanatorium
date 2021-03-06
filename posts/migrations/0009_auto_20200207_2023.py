# Generated by Django 2.2.7 on 2020-02-07 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20200207_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='group',
            field=models.CharField(choices=[(1, 'Пенсионер'), (2, 'Инвалид'), (3, 'Глухонемой'), (4, 'Общество слепых')], default='group', max_length=50),
        ),
        migrations.AlterField(
            model_name='person',
            name='male',
            field=models.CharField(choices=[(1, 'Man'), (2, 'Women')], default='male', max_length=50),
        ),
        migrations.AlterField(
            model_name='person',
            name='pay',
            field=models.CharField(choices=[('Budget', 'Бюджет'), ('Nalik', 'Наличка'), ('Perechesl', 'Перечисление')], max_length=50),
        ),
    ]
