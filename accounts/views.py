from datetime import datetime, timezone
from random import randint

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from accounts.forms import CaptchaFieldForm, MyUserCreationForm, ChangePasswordForm
from accounts.models import MyUser, EmailVerification
from cyber_security.settings import EMAIL_HOST_USER


def login(request):
    context = {"captcha_form": CaptchaFieldForm()}
    if request.user.is_authenticated:
        if request.user:
            return redirect('accounts:home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        form = CaptchaFieldForm(request.POST)
        if not form.is_valid():
            context['captcha_errors'] = "Captcha Not Correct"
            context['email'] = email
            return render(request, 'accounts/login.html', context)

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('accounts:home')
        else:
            context['errors'] = "Email or Password is incorrect"
            context['email'] = email
            return render(request, 'accounts/login.html', context)
    return render(request, 'accounts/login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('accounts:login')


# user register
def register(request):
    if request.user.is_authenticated:
        if request.user:
            return redirect('accounts:home')

    context = {'form': MyUserCreationForm(), "captcha_form": CaptchaFieldForm()}
    if request.method == 'POST':
        email = request.POST.get('email')
        context['email'] = email
        if request.user.is_authenticated:
            return redirect('/')
        form = MyUserCreationForm(request.POST)
        captcha_form = CaptchaFieldForm(request.POST)

        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        if not captcha_form.is_valid():
            context['captcha_errors'] = "Captcha Not Correct"
            context['email'] = email
            context['password'] = password1
            context['password2'] = password2
            return render(request, 'accounts/register.html', context)
        if password1 != password2:
            context['errors'] = 'Password and confirm Password did not match'
            context['email'] = request.POST['email']
            context['password'] = password1
            context['password2'] = password2
            return render(request, 'accounts/register.html', context)
        if form.is_valid():
            form.save()
            email = email
            password = password1
            user = auth.authenticate(email=email, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('accounts:send_email_verification_code')
            else:
                context['errors'] = "something went wrong"
                return render(request, 'accounts/login.html', context)
        else:
            context['errors'] = form.errors
            context['email'] = request.POST['email']
            context['password'] = password1
            context['password2'] = password2
    return render(request, 'accounts/register.html', context)


# sending email verification code
@login_required()
def send_email_verification_code(request):
    user = request.user
    myuser = MyUser.objects.get(email=request.user)
    if myuser.is_email_verified:
        return redirect('/')
    code = randint(100000, 999999)  # verification code
    create_date = datetime.now()
    total_try_requests = 0

    if not EmailVerification.objects.filter(users=user).exists():
        EmailVerification.objects.create(
            users=user,
            verification_code=code,
            created_date_time=create_date,
            total_try_request=total_try_requests,
        )
    else:
        email_verification = EmailVerification.objects.get(users=user)
        block_date = email_verification.block_time
        now = datetime.now(timezone.utc)
        difference = now - block_date
        if difference.total_seconds() < 300:
            return HttpResponse(f'You have been block for {difference} second')
        EmailVerification.objects.filter(users=user).update(
            verification_code=code,
            created_date_time=create_date,
            total_try_request=total_try_requests,
        )
    send_mail(
        "Email Verification Code",
        f"Your email verification code is {code}",
        EMAIL_HOST_USER,
        [EmailVerification.objects.get(users=user).users.email],
    )
    return redirect('accounts:verify_email')


@login_required()
def verify_email(request):
    if MyUser.objects.get(email=request.user).is_email_verified:
        return redirect('accounts:home')
    if request.method == 'POST':
        if MyUser.objects.get(email=request.user).is_email_verified:
            return redirect('accounts:home')

        request_code = request.POST['otp1'] + request.POST['otp2'] + request.POST['otp3'] + request.POST['otp4'] + \
                       request.POST['otp5'] + request.POST['otp6']  # code send from user to verify
        code = EmailVerification.objects.get(users=request.user).verification_code
        if request_code == code:
            MyUser.objects.filter(email=request.user).update(is_email_verified=True)
            return redirect('accounts:home')
        else:
            context = {'error': 'code you have entered is wrong'}
            return render(request, 'accounts/verify_email.html', context)
    return render(request, 'accounts/verify_email.html')


@login_required()
def home(request):
    context = {
        'users': MyUser.objects.all()
    }
    return render(request, 'accounts/home.html',context)


# password change
@login_required()
def password_change(request):
    context = {}
    context['captcha_form'] = CaptchaFieldForm()
    if request.method == 'POST':
        captcha_form = CaptchaFieldForm(request.POST)
        old_password = request.POST['old_password']
        password = request.POST['password']
        password2 = request.POST['password2']
        data = {"password": password, 'password2': password2, "old_password": old_password}
        context['password'] = password
        context['password2'] = password2
        context['old_password'] = old_password
        if not captcha_form.is_valid():
            context['captcha_errors'] = "Captcha Not Correct"
            return render(request, 'accounts/change_password.html', context)

        if not request.user.check_password(old_password):
            context['errors'] = 'Your password didnot match with old password'

            return render(request, 'accounts/change_password.html', context)
        if old_password == password:
            context['errors'] = 'Current password cannot be new password'
            return render(request, 'accounts/change_password.html', context)
        if password != password2:
            context['errors'] = 'your conformed password didnot matched'
            return render(request, 'accounts/change_password.html', context)

        form = ChangePasswordForm(data)
        if form.is_valid():
            MyUser.objects.filter(email=request.user).update(password=form.data['password'])
            messages.success(request,
                             f'Your password has been changed successfully. Please Login with your new password')
            return redirect('/')
        else:
            context['errors'] = form.errors
    return render(request, 'accounts/change_password.html', context)


# password change
def update_password(request, email):
    context = {}
    context['active'] = 'users'
    context['email'] = email
    context['captcha_form'] = CaptchaFieldForm()
    if request.method == 'POST':
        captcha_form = CaptchaFieldForm(request.POST)
        if not captcha_form.is_valid():
            context['captcha_errors'] = "Captcha Not Correct"
            return render(request, 'accounts/admin_update_password.html', context)
        password = request.POST['password']
        password2 = request.POST['password2']
        data = {"password": password, 'password2': password2}
        if password != password2:
            context['errors'] = 'your confirmed password didnot matched'
            return render(request, 'accounts/admin_update_password.html', context)
        form = ChangePasswordForm(data)
        if form.is_valid():
            MyUser.objects.filter(email=email).update(password=form.cleaned_data['password'])
            messages.success(request,
                             f'Password has been changed successfully. Please Login with new password')
            return redirect('accounts:login')
        else:
            context['errors'] = form.errors
    return render(request, 'accounts/admin_update_password.html', context)


def block_user(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
        except:
            email = ''

        user = MyUser.objects.filter(email=email)
        if user.exists():
            user.update(is_blocked=True)
            messages.success(request, f'Email : {email} blocked successfully')
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def unblock_user(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
        except:
            email = ''
        user = MyUser.objects.filter(email=email).filter(is_blocked=True)
        if user.exists():
            user.update(is_blocked=False)
            messages.success(request, f'Email {email} unblocked successfully')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
