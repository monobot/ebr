from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        password = 'admin'

        if User.objects.count() == 0:
            for user in settings.ADMINS:
                username = user[0].replace(' ', '')
                email = user[1]
                admin = User.objects.create_superuser(
                    email=email,
                    username=username,
                    password=password
                )
                admin.is_active = True
                admin.is_admin = True
                admin.save()

            usr = User.objects.create(
                username='plain_user',
                email='plain_user@falso.com',
                first_name='owner_name',
                last_name='owner_last_name',
            )
            usr.is_active = True
            usr.set_password(password)
            usr.save()
