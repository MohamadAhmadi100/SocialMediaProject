from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import password_validation


class UserLoginForm(forms.Form):
    username = forms.CharField(label='', max_length=30,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'نام کاربری، ایمیل یا تلفن'}))
    password = forms.CharField(label='', max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}))


username_errors = {'required': 'این فیلد اجباری است', 'valid': 'نام کاربری قابل قبول نیست'}
email_errors = {'required': 'این فیلد اجباری است', 'valid': 'آدرس ایمیل قابل قبول نیست'}
pass_errors = {'required': 'این فیلد اجباری است', 'valid': 'رمز عبور قابل قبول نیست'}
phone_errors = {'required': 'این فیلد الزامی است', 'valid': 'شماره موبایل را به درستی وارد کنید',
                'min_value': 'یک شماره موبایل واقعی وارد کنید',
                'max_value': 'یک شماره موبایل واقعی وارد کنید'}
code_errors = {'required': 'این فیلد اجباری است', 'valid': 'کد وارد شده صحیح نیست',
               'min_value': 'کد را به درستی وارد کنید',
               'max_value': 'کد را به درستی وارد کنید'}


class UserRegistrationForm(forms.Form):
    username = forms.CharField(error_messages=username_errors, label='', max_length=30,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'نام کاربری'}))
    email = forms.EmailField(error_messages=email_errors, label='', max_length=50,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'آدرس ایمیل'}))
    password = forms.CharField(error_messages=pass_errors, label='', max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}))

    def clean(self):
        password = self.cleaned_data.get('password')
        if password:
            try:
                password_validation.validate_password(password)
            except forms.ValidationError as error:
                self.add_error('password', error)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("کاربری با نام کاربری وارد شده وجود دارد")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("کاربری با ایمیل وارد شده وجود دارد")
        return email


class EditProfile(forms.ModelForm):
    first_name = forms.CharField(label='نام:', max_length=30,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}))
    last_name = forms.CharField(label='نام خانوادگی:', max_length=40,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}))
    email = forms.EmailField(error_messages=email_errors, label='آدرس ایمیل:', max_length=50,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Example@examle.com'}))
    field_order = ('first_name', 'last_name', 'phone', 'bio', 'age', 'email')

    class Meta:
        model = Profile
        fields = ('phone', 'bio', 'age')
        widgets = {
            'bio': forms.Textarea(
                attrs={'class': 'form-control col-md-8', 'placeholder': 'متن پاسخ', 'rows': 2, 'cols': 80,
                       'style': 'resize:none;'}),
            'age': forms.NumberInput(
                attrs={'class': 'form-control col-md-8', 'placeholder': '18'}),
            'phone': forms.NumberInput(
                attrs={'class': 'form-control col-md-8', 'placeholder': '9123223322'}
            )
        }
        labels = {
            'bio': 'بیوگرافی:',
            'age': 'سن:',
            'phone': 'تلفن:'
        }


class PhoneLoginForm(forms.Form):
    phone = forms.IntegerField(error_messages=phone_errors, label='شماره موبایل', min_value=9000000000,
                               max_value=9999999999,
                               widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '9123223322'}))

    def clean_phone(self):
        phone = Profile.objects.filter(phone=self.cleaned_data['phone'])
        if not phone.exists():
            raise forms.ValidationError('کاربری با شماره وارد شده موجود نیست')
        return self.cleaned_data['phone']


class VerifySmsForm(forms.Form):
    code = forms.IntegerField(error_messages=code_errors, label='کد ارسال شده', min_value=100000,
                              max_value=999999,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))


class SmsChangePasswordForm(forms.Form):
    password1 = forms.CharField(label='رمز عبور جدید', max_length=30,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}))
    password2 = forms.CharField(label='تایید رمز عبور جدید', max_length=30,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'تایید رمز عبور جدید'}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(
                'گذر واژه ها منطبق نیستند'
            )
        elif password1:
            try:
                password_validation.validate_password(password1)
            except forms.ValidationError as error:
                self.add_error('password1', error)


class PasswordChangeForm(forms.Form):
    password = forms.CharField(label='رمز عبور فعلی', max_length=30,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': 'رمز عبور فعلی'}))
    password1 = forms.CharField(label='رمز عبور جدید', max_length=30,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور'}))
    password2 = forms.CharField(label='تایید رمز عبور جدید', max_length=30,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'تایید رمز عبور جدید'}))

    def __init__(self, user, data=None):
        self.user = user
        super(PasswordChangeForm, self).__init__(data=data)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(
                'گذر واژه ها منطبق نیستند'
            )
        elif password1:
            try:
                password_validation.validate_password(password1)
            except forms.ValidationError as error:
                self.add_error('password1', error)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError('گذرواژه فعلی مطابقت ندارد')
