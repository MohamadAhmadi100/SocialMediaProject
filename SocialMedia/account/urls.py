from django.urls import path
from .views import (user_login, user_register, user_logout, user_profile, edit_profile, phone_login, verify, follow,
                    unfollow, change_password, sms_change_password)

app_name = 'account'
urlpatterns = [
    path('profile/<int:user_id>/', user_profile, name='profile'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('change-password/', change_password, name='change_password'),
    path('edit-profile/<int:user_id>/', edit_profile, name='edit_profile'),
    path('phone-login/', phone_login, name='phone_login'),
    path('verify/', verify, name='verify'),
    path('v-change-password/', sms_change_password, name='sms_change_password'),
    path('follow/', follow, name='follow'),
    path('unfollow/', unfollow, name='unfollow'),
]
