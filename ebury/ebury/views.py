import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.core.cache import cache
from django.shortcuts import redirect, render

from .forms import UserForm

logger = logging.getLogger('ebury')


def home(request):
    return render(request, 'core.html')


@login_required
def trades(request):
    return render(
        request,
        'trades.html',
        context={'exchanges_cache': str(cache.get('exchanges_cache', {}))}
    )


def register(request):
    logger.debug('iniciado register')
    usuario = User()
    if request.method == 'POST':
        form = UserForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=True)
            logger.debug('register completo redirigiendo')
            return redirect('login')

    else:
        form = UserForm(instance=usuario)
    return render(request, 'register.html', {'form': form, })


@login_required
def change_password(request):
    usuario = request.user
    logger.debug('cambiando clave de {}'.format(usuario.username))
    if request.method == 'POST':
        form = SetPasswordForm(usuario, request.POST)
        if form.is_valid():
            form.save()
            logger.debug('clave cambiada redirigiendo')
            return redirect('login')

    else:
        form = SetPasswordForm(usuario)
    return render(request, 'change_password.html', {'form': form, })
