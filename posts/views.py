from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.template.loader import render_to_string
import json
from datetime import date
from django.views import View
from .models import Post, HashTag, Person
from user_profile.models import User
from posts.forms import PostForm, SearchForm, SearchTagForm, PostFilter, FilterForReport
from django.http import HttpResponse


class Index(View):
    """Не используется"""

    def get(self, request):
        context = {'text': 'Hello, world!'}
        print(context)
        return render(request, 'base.html', context)


class Profile(View):
    """ User Profile Page url: 127.0.0.1:8000/user/<username> """

    def get(self, request, username):
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user)
        posts = Post.objects.filter(user=user)
        form = PostForm()
        context = {
            'posts': posts,
            'user': user,
            'form': form,
        }
        return render(request, 'profile.html', context)


# запись в БД
def create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            date_in = form.cleaned_data['date_in']
            date_out = form.cleaned_data['date_out']
            early_departure = form.cleaned_data['early_departure']
            Person.objects.create(number=form.cleaned_data.get('number'),
                                  date_in=date_in,
                                  date_out=date_out,
                                  company=form.cleaned_data.get('company'),
                                  cab_number=form.cleaned_data.get('cab_number'),
                                  full_name=form.cleaned_data.get('full_name'),
                                  birth_year=form.cleaned_data.get('birth_year'),
                                  passport=form.cleaned_data.get('passport'),
                                  address=form.cleaned_data.get('address'),
                                  early_departure=early_departure,
                                  black_list=form.cleaned_data.get('black_list'),
                                  note=form.cleaned_data.get('note'),
                                  room=form.cleaned_data.get('room'),
                                  phone=form.cleaned_data.get('phone'),
                                  male=form.cleaned_data.get('male'),
                                  group=form.cleaned_data.get('group'),
                                  pay=form.cleaned_data.get('pay'),
                                  )
    return HttpResponseRedirect("/")


# изменение данных в бд
def edit(request, id):
    try:
        person = Person.objects.get(id=id)
        dated = date.today()
        if request.method == "POST":
            person.number = request.POST.get("number")
            person.date_in = request.POST.get("date_in")
            person.date_out = request.POST.get("date_out")
            person.company = request.POST.get("company")
            person.cab_number = request.POST.get("cab_number")
            person.full_name = request.POST.get("full_name")
            person.birth_year = request.POST.get("birth_year")
            person.passport = request.POST.get("passport")
            person.address = request.POST.get("address")
            if request.POST.get("early_departure"):
                person.early_departure = request.POST.get("early_departure")
            else:
                person.early_departure = None

            person.black_list = request.POST.get("black_list")
            person.note = request.POST.get("note")
            person.room = request.POST.get("room")
            person.phone = request.POST.get("phone")
            person.male = request.POST.get("male")
            person.group = request.POST.get("group")
            person.pay = request.POST.get("pay")
            person.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"person": person, 'date': dated})
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


# копирование в БД
def copy(request, id):
    try:
        person = Person.objects.get(id=id)
        dated = date.today()
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                date_in = form.cleaned_data['date_in']
                date_out = form.cleaned_data['date_out']
                early_departure = form.cleaned_data['early_departure']
                Person.objects.create(number=form.cleaned_data.get('number'),
                                      date_in=date_in,
                                      date_out=date_out,
                                      company=form.cleaned_data.get('company'),
                                      cab_number=form.cleaned_data.get('cab_number'),
                                      full_name=form.cleaned_data.get('full_name'),
                                      birth_year=form.cleaned_data.get('birth_year'),
                                      passport=form.cleaned_data.get('passport'),
                                      address=form.cleaned_data.get('address'),
                                      early_departure=early_departure,
                                      black_list=form.cleaned_data.get('black_list'),
                                      note=form.cleaned_data.get('note'),
                                      room=form.cleaned_data.get('room'),
                                      phone=form.cleaned_data.get('phone'),
                                      male=form.cleaned_data.get('male'),
                                      group=form.cleaned_data.get('group'),
                                      pay=form.cleaned_data.get('pay'),
                                      )
            return HttpResponseRedirect("/")
        else:
            return render(request, "copy.html", {"person": person, 'date': dated})
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


# удаление данных из бд
def delete(request, id):
    try:
        person = Person.objects.get(id=id)
        person.delete()
        return HttpResponseRedirect("/")
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


# печать клиента
def print_costumer(request, id):
    person = Person.objects.get(id=id)
    dated = date.today()
    return render(request, "print_costumer.html", {"person": person, 'date': dated})


class PostPost(View):
    """Create Post View"""

    def post(self, request, username):
        form = PostForm(self.request.POST)
        if form.is_valid():
            user = User.objects.get(username=username)
            post = Post(text=form.cleaned_data['text'], user=user)
            post.save()
            words = form.cleaned_data['text'].split(" ")
            for word in words:
                if word.startswith('#'):
                    hash_tag, created = HashTag.objects.get_or_create(name=word)
                    hash_tag.post.add(post)
        return HttpResponseRedirect('/user/' + username)


class Search(View):
    """ Index """
    def get(self, request):
        dated = date.today()
        form = SearchForm()
        forma_v = PostForm()
        people = Person.objects.order_by("number")
        filter_f = PostFilter()
        form_for_report = FilterForReport()
        context = {'search': form, 'forma_v': forma_v, 'people': people, 'date': dated, 'filter': filter_f, 'form_for_report': form_for_report}
        return render(request, 'index.html', context)

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data['q']
            posts = Person.objects.filter(full_name__icontains=q)
            context = {'q': q, 'posts': posts}
            return_str = render_to_string('part_views/_post_search.html', context)
            return HttpResponse(json.dumps(return_str), content_type='application/json')
        else:
            HttpResponseRedirect("/search")


class SearchTag(View):
    """ Search tags with autocomplete (live search) """
    def get(self, request):
        forma_v = PostForm()
        people = Person.objects.all()
        form = SearchTagForm()
        context = {'searchtag': form, 'forma_v': forma_v, 'people': people}
        return render(request, 'search_tags.html', context)

    def post(self, request):
        q = request.POST['q']
        form = SearchTagForm()
        tags = Person.objects.filter(full_name__icontains=q)
        context = {'tags': tags, 'searchtag': form}
        return render(request, 'search_tags.html', context)


# фильтр всех клиентов
def filter_peoples(request):
    dated = date.today()
    form_of_filter = PostFilter(request.GET)
    if form_of_filter.is_valid():
        male = form_of_filter.cleaned_data['male']
        group = form_of_filter.cleaned_data['group']
        pay = form_of_filter.cleaned_data['pay']
        date_in = form_of_filter.cleaned_data['date_in']
        date_out = form_of_filter.cleaned_data['date_out']
        if male != 'Все' and group != 'Все' and pay != 'Все':
            posts = Person.objects.filter(male=male, group=group, pay=pay)
        elif male != 'Все' and group != 'Все':
            posts = Person.objects.filter(male=male, group=group)
        elif pay != 'Все' and group != 'Все':
            posts = Person.objects.filter(pay=pay, group=group)
        elif pay != 'Все' and male != 'Все':
            posts = Person.objects.filter(pay=pay, male=male)
        elif male != 'Все':
            posts = Person.objects.filter(male=male)
        elif group != 'Все':
            posts = Person.objects.filter(group=group)
        elif pay != 'Все':
            posts = Person.objects.filter(pay=pay)
        else:
            posts = Person.objects.all()

        if date_in:
            posts = posts.filter(date_in__gte=date_in)
        if date_out:
            posts = posts.filter(date_out__lte=date_out)

        sorted_posts = posts.order_by("number")
        context = {'posts': sorted_posts, 'male': male, 'group': group, 'pay': pay, 'date': dated, 'posts_all': posts,
                   'date_in': date_in, 'date_out': date_out}
        return render(request, 'filter_peoples.html', context)
    else:
        HttpResponseRedirect("/")


# фильтр для отчета
def report(request):
    dated = date.today()
    form_for_report = FilterForReport(request.GET)
    if form_for_report.is_valid():
        date_in = form_for_report.cleaned_data['date_in']
        date_out = form_for_report.cleaned_data['date_out']

        if date_in and date_out:
            posts = Person.objects.filter(date_in__gte=date_in, date_in__lte=date_out)
        elif date_in:
            posts = Person.objects.filter(date_in__gte=date_in)
        elif date_out:
            posts = Person.objects.filter(date_in__lte=date_out)
        else:
            posts = Person.objects.all()

        january = posts.filter(date_in__month='01')
        february = posts.filter(date_in__month='02')
        march = posts.filter(date_in__month='03')
        april = posts.filter(date_in__month='04')
        may = posts.filter(date_in__month='05')
        june = posts.filter(date_in__month='06')
        jule = posts.filter(date_in__month='07')
        august = posts.filter(date_in__month='08')
        september = posts.filter(date_in__month='09')
        october = posts.filter(date_in__month='10')
        november = posts.filter(date_in__month='11')
        december = posts.filter(date_in__month='12')

        def male_m(month):
            month = month.filter(male='Мужской')
            if month:
                return month.count
            else:
                return ''

        def male_w(month):
            month = month.filter(male='Женский')
            if month:
                return month.count
            else:
                return ''

        def group_none(month):
            month = month.filter(group='Неизвестно')
            if month:
                return month.count
            else:
                return ''

        def group_invalid(month):
            month = month.filter(group='Инвалид')
            if month:
                return month.count
            else:
                return ''

        def group_pension(month):
            month = month.filter(group='Пенсионер')
            if month:
                return month.count
            else:
                return ''

        def group_slepie(month):
            month = month.filter(group='Общество слепых')
            if month:
                return month.count
            else:
                return ''

        def group_gluhie(month):
            month = month.filter(group='Глухонемой')
            if month:
                return month.count
            else:
                return ''

        def pay_none(month):
            month = month.filter(pay='Неизвестно')
            if month:
                return month.count
            else:
                return ''

        def pay_budget(month):
            month = month.filter(pay='Бюджет')
            if month:
                return month.count
            else:
                return ''

        def pay_nal(month):
            month = month.filter(pay='Наличка')
            if month:
                return month.count
            else:
                return ''

        def pay_pall(month):
            month = month.filter(pay='Перечисление')
            if month:
                return month.count
            else:
                return ''

        context = {'posts': posts,
                   'date': dated,
                   'date_in': date_in,
                   'date_out': date_out,
                   'january': january,
                   'february': february,
                   'march': march,
                   'april': april,
                   'may': may,
                   'june': june,
                   'jule': jule,
                   'august': august,
                   'september': september,
                   'october': october,
                   'november': november,
                   'december': december,

                   'january_male_m': male_m(january),
                   'january_male_w': male_w(january),
                   'february_male_m': male_m(february),
                   'february_male_w': male_w(february),
                   'march_male_m': male_m(march),
                   'march_male_w': male_w(march),
                   'april_male_m': male_m(april),
                   'april_male_w': male_w(april),
                   'may_male_m': male_m(may),
                   'may_male_w': male_w(may),
                   'june_male_m': male_m(june),
                   'june_male_w': male_w(june),
                   'jule_male_m': male_m(jule),
                   'jule_male_w': male_w(jule),
                   'august_male_m': male_m(august),
                   'august_male_w': male_w(august),
                   'september_male_m': male_m(september),
                   'september_male_w': male_w(september),
                   'october_male_m': male_m(october),
                   'october_male_w': male_w(october),
                   'november_male_m': male_m(november),
                   'november_male_w': male_w(november),
                   'december_male_m': male_m(december),
                   'december_male_w': male_w(december),
                   'all_male_m': male_m(posts),
                   'all_male_w': male_w(posts),

                   'january_group_none': group_none(january),
                   'february_group_none': group_none(february),
                   'march_group_none': group_none(march),
                   'april_group_none': group_none(april),
                   'may_group_none': group_none(may),
                   'june_group_none': group_none(june),
                   'jule_group_none': group_none(jule),
                   'august_group_none': group_none(august),
                   'september_group_none': group_none(september),
                   'october_group_none': group_none(october),
                   'november_group_none': group_none(november),
                   'december_group_none': group_none(december),
                   'all_group_none': group_none(posts),

                   'january_group_invalid': group_invalid(january),
                   'february_group_invalid': group_invalid(february),
                   'march_group_invalid': group_invalid(march),
                   'april_group_invalid': group_invalid(april),
                   'may_group_invalid': group_invalid(may),
                   'june_group_invalid': group_invalid(june),
                   'jule_group_invalid': group_invalid(jule),
                   'august_group_invalid': group_invalid(august),
                   'september_group_invalid': group_invalid(september),
                   'october_group_invalid': group_invalid(october),
                   'november_group_invalid': group_invalid(november),
                   'december_group_invalid': group_invalid(december),
                   'all_group_invalid': group_invalid(posts),

                   'january_group_pension': group_pension(january),
                   'february_group_pension': group_pension(february),
                   'march_group_pension': group_pension(march),
                   'april_group_pension': group_pension(april),
                   'may_group_pension': group_pension(may),
                   'june_group_pension': group_pension(june),
                   'jule_group_pension': group_pension(jule),
                   'august_group_pension': group_pension(august),
                   'september_group_pension': group_pension(september),
                   'october_group_pension': group_pension(october),
                   'november_group_pension': group_pension(november),
                   'december_group_pension': group_pension(december),
                   'all_group_pension': group_pension(posts),

                   'january_group_slepie': group_slepie(january),
                   'february_group_slepie': group_slepie(february),
                   'march_group_slepie': group_slepie(march),
                   'april_group_slepie': group_slepie(april),
                   'may_group_slepie': group_slepie(may),
                   'june_group_slepie': group_slepie(june),
                   'jule_group_slepie': group_slepie(jule),
                   'august_group_slepie': group_slepie(august),
                   'september_group_slepie': group_slepie(september),
                   'october_group_slepie': group_slepie(october),
                   'november_group_slepie': group_slepie(november),
                   'december_group_slepie': group_slepie(december),
                   'all_group_slepie': group_slepie(posts),

                   'january_group_gluhie': group_gluhie(january),
                   'february_group_gluhie': group_gluhie(february),
                   'march_group_gluhie': group_gluhie(march),
                   'april_group_gluhie': group_gluhie(april),
                   'may_group_gluhie': group_gluhie(may),
                   'june_group_gluhie': group_gluhie(june),
                   'jule_group_gluhie': group_gluhie(jule),
                   'august_group_gluhie': group_gluhie(august),
                   'september_group_gluhie': group_gluhie(september),
                   'october_group_gluhie': group_gluhie(october),
                   'november_group_gluhie': group_gluhie(november),
                   'december_group_gluhie': group_gluhie(december),
                   'all_group_gluhie': group_gluhie(posts),

                   'january_pay_none': pay_none(january),
                   'february_pay_none': pay_none(february),
                   'march_pay_none': pay_none(march),
                   'april_pay_none': pay_none(april),
                   'may_pay_none': pay_none(may),
                   'june_pay_none': pay_none(june),
                   'jule_pay_none': pay_none(jule),
                   'august_pay_none': pay_none(august),
                   'september_pay_none': pay_none(september),
                   'october_pay_none': pay_none(october),
                   'november_pay_none': pay_none(november),
                   'december_pay_none': pay_none(december),
                   'all_pay_none': pay_none(posts),

                   'january_pay_budget': pay_budget(january),
                   'february_pay_budget': pay_budget(february),
                   'march_pay_budget': pay_budget(march),
                   'april_pay_budget': pay_budget(april),
                   'may_pay_budget': pay_budget(may),
                   'june_pay_budget': pay_budget(june),
                   'jule_pay_budget': pay_budget(jule),
                   'august_pay_budget': pay_budget(august),
                   'september_pay_budget': pay_budget(september),
                   'october_pay_budget': pay_budget(october),
                   'november_pay_budget': pay_budget(november),
                   'december_pay_budget': pay_budget(december),
                   'all_pay_budget': pay_budget(posts),

                   'january_pay_nal': pay_nal(january),
                   'february_pay_nal': pay_nal(february),
                   'march_pay_nal': pay_nal(march),
                   'april_pay_nal': pay_nal(april),
                   'may_pay_nal': pay_nal(may),
                   'june_pay_nal': pay_nal(june),
                   'jule_pay_nal': pay_nal(jule),
                   'august_pay_nal': pay_nal(august),
                   'september_pay_nal': pay_nal(september),
                   'october_pay_nal': pay_nal(october),
                   'november_pay_nal': pay_nal(november),
                   'december_pay_nal': pay_nal(december),
                   'all_pay_nal': pay_nal(posts),

                   'january_pay_pall': pay_pall(january),
                   'february_pay_pall': pay_pall(february),
                   'march_pay_pall': pay_pall(march),
                   'april_pay_pall': pay_pall(april),
                   'may_pay_pall': pay_pall(may),
                   'june_pay_pall': pay_pall(june),
                   'jule_pay_pall': pay_pall(jule),
                   'august_pay_pall': pay_pall(august),
                   'september_pay_pall': pay_pall(september),
                   'october_pay_pall': pay_pall(october),
                   'november_pay_pall': pay_pall(november),
                   'december_pay_pall': pay_pall(december),
                   'all_pay_pall': pay_pall(posts),
                   }
        return render(request, 'report.html', context)
    else:
        HttpResponseRedirect("/")


class TagJson(View):
    """ Search tags with autocomplete (live search) json data"""

    def get(self, request):
        q = request.GET.get('q', '')
        taglist = []
        tags = Person.objects.filter(full_name__icontains=q)
        for tag in tags:
            new = {'q': tag.full_name, 'count': int(len(tags.all()))}
            taglist.append(new)
        return HttpResponse(json.dumps(taglist), content_type="application/json")
