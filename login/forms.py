from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label='username', max_length=128, error_messages={'required': ''})
    password = forms.CharField(label='password', max_length=256, widget=forms.PasswordInput)
    captcha = CaptchaField(label='captcha')

class RegisterForm(forms.Form):
    gender = (('male', 'male'), ('female', 'female'))
    username = forms.CharField(label='username', max_length=128)
    password1 = forms.CharField(label='password', max_length=256, widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', max_length=256, widget=forms.PasswordInput)
    email = forms.EmailField(label = 'email', widget=forms.EmailInput)
    sex = forms.ChoiceField(label='gender', choices=gender)
    captcha = CaptchaField(label='captcha')