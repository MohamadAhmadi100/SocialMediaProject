from django.shortcuts import render, redirect, get_object_or_404
from .forms import (
    UserLoginForm, UserRegistrationForm, EditProfile, PhoneLoginForm, VerifySmsForm, PasswordChangeForm,
    SmsChangePasswordForm)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from posts.models import Post
from django.contrib.auth.decorators import login_required
from random import randint
from kavenegar import *
from .models import Profile, Relation
from django.http import JsonResponse


def user_login(request):
    next = request.GET.get('next')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user_e = User.objects.get(email=cd['username'])
            except:
                user_e = None
            user = authenticate(request, username=cd['username'], password=cd['password'])
            user_by_email = authenticate(request, username=user_e, password=cd['password'])
            if user or user_by_email:
                if user is not None:
                    login(request, user)
                    messages.success(request, f"{user} خوش آمدبد ", 'success')
                elif user_by_email is not None:
                    login(request, user_by_email)
                    messages.success(request, f"{user_by_email} خوش آمدبد ", 'success')
                if next:
                    return redirect(next)
                return redirect('posts:all_posts')
            else:
                messages.error(request, 'کاربری با مشخصات ورودی پیدا نشد', 'danger')
    else:
        form = UserLoginForm()
    return render(request, 'account/user_login.html', {'form': form})


def phone_login(request):
    if request.method == 'POST':
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            global phone, verify_code
            phone = form.cleaned_data['phone']
            z_phone = f"0{phone}"
            verify_code = randint(100000, 999999)
            api = KavenegarAPI(
                '33634D686D584A777941332F536D79306A765947675A5A592F51745137516661555943734D2B6C73414C673D')
            params = {'sender': '', 'receptor': z_phone, 'message': f"کد ورود به سایت جنگو: {verify_code}"}
            try:
                api.sms_send(params)
                return redirect('account:verify')
            except:
                messages.error(request, 'مشکلی بوجود آمد، لطفا مجددا تلاش کنید', 'danger')
                form = PhoneLoginForm()
    else:
        form = PhoneLoginForm()
    return render(request, 'account/phone_login.html', {'form': form})


def verify(request):
    if request.method == 'POST':
        form = VerifySmsForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['code'] == verify_code:
                global verified_user
                profile = get_object_or_404(Profile, phone=phone)
                verified_user = get_object_or_404(User, profile__id=profile.id)
                login(request, verified_user)
                messages.success(request, f"{verified_user} خوش آمدید", 'success')
                return redirect('account:sms_change_password')
            else:
                messages.error(request, 'کد وارد شده صحیح نیست', 'danger')

    else:
        form = VerifySmsForm()
    return render(request, 'account/verify.html', {'form': form})


@login_required
def sms_change_password(request):
    if request.method == 'POST':
        form = SmsChangePasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            verified_user.set_password(cd['password1'])
            verified_user.save()
            login(request, verified_user)
            messages.success(request, 'گذرواژه با موفقیت تغییر کرد', 'success')
            return redirect('account:profile', verified_user.id)
    else:
        form = SmsChangePasswordForm()
    return render(request, 'account/sms_change_password.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            # user = authenticate(request, username=request.user, password=cd['password'])
            # if user is not None:
            user = get_object_or_404(User, pk=request.user.id)
            user.set_password(cd['password1'])
            user.save()
            login(request, user)
            messages.success(request, 'گذرواژه با موفقیت تغییر کرد', 'success')
            return redirect('account:profile', user.id)
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'account/change_password.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
            login(request, user)
            messages.success(request, f"{user} ثبت نام شما با موفقیت انجام شد")
            return redirect('posts:all_posts')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/user_register.html', {'form': form})


@login_required
def user_logout(request):
    messages.info(request, f"{request.user} با موفقیت خارج شدید")
    logout(request)
    return redirect('posts:all_posts')


@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    posts = Post.objects.filter(user=user)
    relation = Relation.objects.filter(from_user=request.user, to_user=user)
    is_following = False
    if relation.exists():
        is_following = True
    self_profile = False
    if request.user.id == user_id:
        self_profile = True
    return render(request, 'account/user_profile.html',
                  {'user': user, 'posts': posts, 'self_profile': self_profile, 'is_following': is_following})


@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.user.id == user_id:
        if request.method == 'POST':
            form = EditProfile(request.POST, instance=user.profile)
            if form.is_valid():
                form.save()
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.save()
                messages.success(request, 'پروفایل شما با موفقیت ویرایش شد', 'success')
                return redirect('account:profile', user_id)
        else:
            form = EditProfile(instance=user.profile,
                               initial={'first_name': user.first_name, 'last_name': user.last_name,
                                        'email': user.email})
        return render(request, 'account/edit_profile.html', {'form': form})


@login_required
def follow(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        following_user = get_object_or_404(User, pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=following_user)
        if relation.exists():
            return JsonResponse({'status': 'exists'})
        else:
            Relation(from_user=request.user, to_user=following_user).save()
            return JsonResponse({'status': 'OK'})


@login_required
def unfollow(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        following_user = get_object_or_404(User, pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=following_user)
        if relation.exists():
            relation.delete()
            return JsonResponse({'status': 'OK'})
        else:
            return JsonResponse({'status': 'not_exists'})
