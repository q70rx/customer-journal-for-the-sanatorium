from datetime import date

from django.db import models
from user_profile.models import User


class Post(models.Model):
    ''' Post model '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=30, default='Global')
    is_active = models.BooleanField(default=True)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:50]


class HashTag(models.Model):
    ''' HashTag model '''
    name = models.CharField(max_length=100, unique=True)
    post = models.ManyToManyField(Post)

    def __str__(self):
        return self.name


class Person(models.Model):
    MALE = [
        ("Мужской", "Мужской"),
        ("Женский", "Женский"),
    ]
    GROUP = [
        ('Неизвестно', 'Неизвестно'),
        ("Пенсионер", "Пенсионер"),
        ("Инвалид", "Инвалид"),
        ("Глухонемой", "Глухонемой"),
        ("Общество слепых", "Общество слепых"),
    ]
    PAY = [
        ('Неизвестно', 'Неизвестно'),
        ('Бюджет', "Бюджет"),
        ('Наличка', "Наличка"),
        ('Перечисление', "Перечисление"),
    ]
    BLACK_LIST = [
        ('Неизвестно', 'Неизвестно'),
        ('Белый', 'Белый'),
        ('Черный', 'Черный'),
    ]
    number = models.CharField(default=1, max_length=20, help_text='№ пут. листа', null=True, blank=True)
    date_in = models.DateField(default=date.today, max_length=20, null=True, blank=False)
    date_out = models.DateField(default=date.today, max_length=20, null=True, blank=False)
    company = models.CharField(default='New company', max_length=50, help_text='Организация')
    cab_number = models.CharField(default='Cab. number', max_length=5, help_text='№ каб. врача')
    full_name = models.CharField(default='Full name', max_length=100, help_text='ФИО клиента', null=True, blank=True)
    birth_year = models.CharField(default='Birth YEAR', max_length=12, help_text='Год рождения')
    passport = models.CharField(default='Passport', max_length=50, help_text='Паспорт / пенсионное')
    address = models.CharField(default='Address', max_length=200, help_text='Домашний адресс')
    early_departure = models.DateField(default='Departure', max_length=20, null=True, blank=True)
    black_list = models.CharField(max_length=20, choices=BLACK_LIST, default='black_list')
    note = models.CharField(default='Notes', max_length=500, help_text='Комментарий', null=True, blank=True)
    room = models.CharField(default='room', max_length=10, help_text='Room', null=True, blank=True)
    phone = models.CharField(default='phone', max_length=20, help_text='phone', null=True, blank=True)
    male = models.CharField(max_length=20, choices=MALE, default='male')
    group = models.CharField(max_length=20, choices=GROUP, default='group')
    pay = models.CharField(max_length=20, choices=PAY, default='pay')

    def __str__(self):
        return self.full_name
