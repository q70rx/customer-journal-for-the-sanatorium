from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.template.loader import render_to_string
import json
from datetime import date
from django.http import HttpResponse
from django.views import View
from .models import Post, HashTag, Person
from user_profile.models import User
from posts.forms import PostForm, SearchForm, SearchTagForm, PostFilter
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
            person.early_departure = request.POST.get("early_departure")
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
    """ Search all posts url: 127.0.0.1:8000/search/?q=<q>"""
    def get(self, request):
        dated = date.today()
        form = SearchForm()
        forma_v = PostForm()
        people = Person.objects.all()
        filter_f = PostFilter()
        context = {'search': form, 'forma_v': forma_v, 'people': people, 'date': dated, 'filter': filter_f}
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


def sfilter(request):
    dated = date.today()
    s_filter = PostFilter(request.POST)
    if s_filter.is_valid():
        male = s_filter.cleaned_data['male']
        group = s_filter.cleaned_data['group']
        pay = s_filter.cleaned_data['pay']
        # mouth = s_filter.cleaned_data['mouth']
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

        reverse_posts = reversed(posts)
        context = {'posts': reverse_posts, 'male': male, 'group': group, 'pay': pay, 'date': dated, 'posts_all': posts}
        return render(request, 'sfilter.html', context)
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
