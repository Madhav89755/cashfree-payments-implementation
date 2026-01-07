from django.urls import path
from .views import home, login_user, register, verify_otp, dashboard, logout_user

urlpatterns=[
    path('', home, name='home-page'),
    path('login/', login_user, name='login-page'),
    path('register/', register, name='register-page'),
    path('verify-otp/', verify_otp, name="verify-otp"),
    path('dashboard/', dashboard, name="dashboard"),
    path('logout/', logout_user, name="logout"),
]