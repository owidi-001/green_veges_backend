from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (RegisterUser, UserLogin, ResetPasswordView, ResetPasswordCompleteView, UserProfileView)

urlpatterns = [
    # Auth user
    path("auth/register/", RegisterUser.as_view(), name="register"),
    path("auth/login/", UserLogin.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name="logout"),

    # profile
    path("auth/profile/", UserProfileView.as_view(), name="update"),

    # reset password done
    path("auth/password/reset_password/", ResetPasswordView.as_view(), name="reset"),
    path("auth/password/reset_password_complete/<uidb64>/<token>/", ResetPasswordCompleteView.as_view(), name="reset"),
]
