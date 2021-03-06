# Generated by Django 3.0.2 on 2020-01-31 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('location', models.CharField(default='Global', max_length=30)),
                ('is_active', models.BooleanField(default=True)),
                ('is_favorite', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.User')),
            ],
        ),
    ]
