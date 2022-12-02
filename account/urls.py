from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path

from account.views import dashboard, user_login

urlpatterns = [
    # path("login/", user_login, name="login"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password-change/", PasswordChangeView.as_view(), name="password_change"),
    path("password-change/done/", PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("", dashboard, name="dashboard"),
]
