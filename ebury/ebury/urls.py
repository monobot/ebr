from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout

from .views import home, trades, register, change_password


urlpatterns = [
    url(r'^administration/', admin.site.urls),
    url(r'^api/', include('api.urls', namespace='api')),

    url(r'register/$', register, name='register'),
    url(r'change_password/$', change_password, name='change_password'),

    url(r'login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'logout/$', logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^trades/$', trades, name='trades'),
    url(r'^$', home, name='home'),
]
