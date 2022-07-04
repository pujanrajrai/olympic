from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.hashers import make_password

from accounts.models import MyUser


class CaptchaFieldForm(forms.Form):
    captcha = CaptchaField()


def password_check(password):
    error_list = []
    special_sym = ['$', '@', '#', '%']
    if len(password) < 8:
        error_list.append('Password Length should be at least 8.')
    if not any(char.isdigit() for char in password):
        error_list.append('Password should have at least one numeral.')

    if not any(char.isupper() for char in password):
        error_list.append('Password should have at least one uppercase letter.')
    if not any(char.islower() for char in password):
        error_list.append('Password should have at least one lowercase letter.')

    if not any(char in special_sym for char in password):
        error_list.append('Password should have at least one of the symbols $@#')
    if not error_list:
        return make_password(password)
    else:
        return error_list


class MyUserCreationForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['email', 'password']

    def clean_password(self):
        password = self.cleaned_data['password']
        check_password = password_check(password)
        if isinstance(check_password, list):
            raise forms.ValidationError(check_password)
        else:
            return check_password


class ChangePasswordForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ["password"]

    def clean_password(self):
        password = self.cleaned_data['password']
        check_password = password_check(password)
        if isinstance(check_password, list):
            raise forms.ValidationError(check_password)
        else:
            return check_password
