from django.conf.urls import url
from django.views.decorators.csrf import ensure_csrf_cookie

from api.views import TradesView


urlpatterns = [
    url(
        r'^trades/$',
        ensure_csrf_cookie(TradesView.as_view(
            {'get': 'list', 'post': 'create', }
        )),
        name='trades'
    ),
]
