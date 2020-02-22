from django import forms
from datetime import date
from django.forms import SelectDateWidget


class PostForm(forms.Form):
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
    full_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "my_field"}))
    number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "my_field"}))
    date_in = forms.DateField(widget=SelectDateWidget, initial=date.today, help_text='Дата С')
    date_out = forms.DateField(widget=SelectDateWidget, initial=date.today, help_text='Дата ПО')
    company = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "my_field"}))
    cab_number = forms.CharField(max_length=5, widget=forms.TextInput(attrs={"class": "my_field"}))
    birth_year = forms.CharField(max_length=12, widget=forms.TextInput(attrs={"class": "my_field"}))
    passport = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "my_field"}))
    address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"class": "my_field"}))
    early_departure = forms.DateField(required=False, widget=SelectDateWidget, initial=date.today)
    black_list = forms.ChoiceField(choices=BLACK_LIST)
    note = forms.CharField(required=False, max_length=500, widget=forms.TextInput(attrs={"class": "my_field"}))
    room = forms.CharField(required=False, max_length=10, widget=forms.TextInput(attrs={"class": "my_field"}))
    phone = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={'class': 'my_field'}))
    male = forms.ChoiceField(choices=MALE)
    group = forms.ChoiceField(choices=GROUP)
    pay = forms.ChoiceField(choices=PAY)


class PostFilter(forms.Form):
    MALE = [
        ("Все", "Все"),
        ("Мужской", "Мужской"),
        ("Женский", "Женский"),
    ]
    GROUP = [
        ("Все", "Все"),
        ('Неизвестно', 'Неизвестно'),
        ("Пенсионер", "Пенсионер"),
        ("Инвалид", "Инвалид"),
        ("Глухонемой", "Глухонемой"),
        ("Общество слепых", "Общество слепых"),
    ]
    PAY = [
        ("Все", "Все"),
        ('Неизвестно', 'Неизвестно'),
        ('Бюджет', "Бюджет"),
        ('Наличка', "Наличка"),
        ('Перечисление', "Перечисление"),
    ]
    male = forms.ChoiceField(choices=MALE)
    group = forms.ChoiceField(choices=GROUP)
    pay = forms.ChoiceField(choices=PAY)
    date_in = forms.DateField(widget=SelectDateWidget, required=False)
    date_out = forms.DateField(widget=SelectDateWidget, required=False)


class FilterForReport(forms.Form):
    date_in = forms.DateField(widget=SelectDateWidget, required=False)
    date_out = forms.DateField(widget=SelectDateWidget, required=False)


class SearchForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput(attrs={
        'size': 50,
        'class': 'form-control search-query',
        'autofocus': 'autofocus',
        'placeholder': 'Поиск по ФИО'
    }))


class SearchTagForm(forms.Form):
    q = forms.CharField(widget=forms.TextInput(attrs={
        'size': 50,
        'class': 'form-control search-tag-query typeahead',
        'id': 'typeahead',
        'autofocus': 'autofocus',
        'placeholder': 'Поиск по ФИО'
    }))
