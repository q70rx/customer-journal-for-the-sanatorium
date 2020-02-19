# Generated by Django 2.2.7 on 2020-02-07 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20200207_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='group',
            field=models.CharField(choices=[(1, 'Пенсионер'), (2, 'Инвалид'), (3, 'Глухонемой'), (4, 'Общество слепых')], default='group', help_text='group', max_length=50),
        ),
        migrations.AlterField(
            model_name='person',
            name='male',
            field=models.CharField(choices=[(1, 'Man'), (2, 'Women')], default='male', help_text='male', max_length=50),
        ),
        migrations.AlterField(
            model_name='person',
            name='pay',
            field=models.CharField(choices=[(1, 'Бюджет'), (2, 'Наличка'), (3, 'Перечисление')], default='pay', help_text='pay', max_length=50),
        ),
    ]
