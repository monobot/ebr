from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    class Meta:
        fields = ('username',)
        model = User

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.is_active = True
        user.set_password(self.cleaned_data['password1'])
        user.save()

        return user
