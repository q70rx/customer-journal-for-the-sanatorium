# from django.contrib import admin
# from django.urls import path
# from posts import views
# from posts.views import Index, Profile, PostPost
# # from user_profile.views import User
# from django.conf.urls import url
#
# #7/8:00
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # path('', views.index, name='index'),
#     path('', Index.as_view(), name='index'),
#     url(r'^user/(\w+)/$', Profile.as_view()),
#     url(r'^user/(\w+)/post/$', PostPost.as_view())
# ]

"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))

Символ/выражение 	Совпадающая строка
. (Точка) 	         Любой символ
^ (Каретка)          Начало строки
$ 	                 Конец строки
* 	                 0 или более повторений
+ 	                 1 или более повторений
? 	                 0 или 1 повторение
| 	                 A | B означает A или B
[a-z] 	             Любая буква в нижнем регистре
\w 	                 Любой цифробуквенный символ или _ _
\d 	                 Любая цифра
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from posts import views
from posts.views import Index, Profile, PostPost, Search, SearchTag, TagJson


urlpatterns = [
    path('edit/<int:id>/', views.edit),
    path('copy/<int:id>/', views.copy),
    path('delete/<int:id>/', views.delete),
    path('filter/', views.sfilter),
    url(r'^admin/', admin.site.urls),
    url(r'^create/', views.create),
    url(r'^$', Search.as_view()),
    url(r'^user/(\w+)/$', Profile.as_view()),
    url(r'^user/(\w+)/post/$', PostPost.as_view()),
    url(r'^search/$', Search.as_view()),
    url(r'^search/hashtag$', SearchTag.as_view()),
    url(r'^hashtag.json$', TagJson.as_view()),
]
