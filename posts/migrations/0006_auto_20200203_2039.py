# Generated by Django 2.2.7 on 2020-02-03 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20200203_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='number',
            field=models.CharField(blank=True, default=1, help_text='№ пут. листа', max_length=20, null=True),
        ),
    ]
