from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (RegisterUser, UserLogin, ResetPasswordView, ResetPasswordCompleteView)

urlpatterns = [
    # Auth user
    path("auth/register/", RegisterUser.as_view(), name="register"),
    path("auth/login/", UserLogin.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name="logout"),

    # reset password done
    path("auth/reset_password/", ResetPasswordView.as_view(), name="reset"),
    path("auth/reset_password_complete/<uidb64>/<token>/", ResetPasswordCompleteView.as_view(), name="reset"),

]