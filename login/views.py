from django.shortcuts import render, HttpResponse, redirect
from . import models
from . import forms
import hashlib, datetime
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives


def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code = code, user = user)
    return code

def send_email(email, code):
    subject = 'Verification email from Jing Zou\'s test site!'
    text_content = 'Thank you for register an account on Jing Zou\'s test site!'  # used replace html when it is invalid
    html_content = '''
            <p>Thank you for register an account on Jing Zou\'s test site! Please click the <a href="http://{}/confirm/?code={}" target=blank>verification link</a> to complete your registration!</p>
            <p>This link is valid for {} days!</p>
        '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# Create your views here.
def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = 'Please check your username and password!'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(name = username)
            except:
                message = 'Username not exists!'
                return render(request, 'login/login.html', locals())
            if not user.has_confirmed:
                message = 'Verification required!'
                return render(request, 'login/login.html', locals())
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = 'Wrong password!'
                return render(request, 'login/login.html', locals())

        return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())

def index(request):
    if request.session.get('is_login', None):
        return render(request, 'login/index.html')
    return redirect('/login/')

def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = 'Please check your information!'
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            gender = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = 'Unmatched passwords!'
                return render(request, 'login/register.html', locals())
            exist_users = models.User.objects.filter(name = username)
            if exist_users:
                message = 'Username already exists!'
                return render(request, 'login/register.html', locals())
            exist_emails = models.User.objects.filter(email = email)
            if exist_emails:
                message = 'Email already exists!'
                return render(request, 'login/register.html', locals())

            # data = {'name': username, 'password': hash_code(password1), 'email': email, 'sex': gender}
            # models.User.objects.create(**data)
            new_user = models.User()
            new_user.name = username
            new_user.password = hash_code(password1)
            new_user.email = email
            new_user.sex = gender
            new_user.save()

            code = make_confirm_string(new_user)
            send_email(email, code)

            message = 'Please check your confirmation email!'
            return render(request, 'login/confirm.html', locals())

        return render(request, 'login/register.html', locals())

    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())

def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code = code)
    except:
        message = 'Invalid verification request!'
        return render(request, 'login/confirm.html', locals())
    c_time = confirm.c_time
    now = datetime.datetime.now()
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        message = 'Your verification code has expired! Please register again!'
        return render(request, 'login/confirm.html', locals())
    confirm.user.has_confirmed = True
    confirm.user.save()
    confirm.delete()
    message = 'You account has successfully verified! Please login now!'
    return render(request, 'login/confirm.html', locals())

def logout(request):
    if request.session.get('is_login', None):
        request.session.flush()
        # you can also use
        # del request.session['is_login']
        # del request.session['user_id']
        # del request.session['user_name']
    return redirect('/login/')