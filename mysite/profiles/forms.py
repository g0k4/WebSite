from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
        )


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'image',
        )

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = False