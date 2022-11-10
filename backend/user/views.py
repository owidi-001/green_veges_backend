import random
from threading import Thread

from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import UserLoginForm, UserCreationForm, ResetPasswordForm, UserUpdateForm
from .send_email import send_mail
from .serializers import *
from .token_generator import password_reset_token
# Documentation schema
from .schema import *


class EmailThead(Thread):
    def __init__(self, email_to, message, subject):
        super().__init__()
        self.email_to = email_to
        self.message = message
        self.subject = subject

    def run(self):
        send_mail(self.message, self.email_to, self.subject)


# users
@method_decorator(csrf_exempt, name='dispatch')
class RegisterUser(APIView):
    """
        The user fills the required parameters namely (email,password,username and phone number).
        The form is checked for validity and user saved if valid otherwise relevant exception is thrown.
    """
    schema = RegistrationSchema()

    def post(self, request):
        # print(request.data)
        form = UserCreationForm(request.data)

        if form.is_valid():
            user = form.save()
            data = UserSerializer(user).data
            # create auth token
            token = Token.objects.get(user=user).key
            data["token"] = token
            email_to = form.cleaned_data.get("email")
            scheme = request.build_absolute_uri().split(":")[0]
            path = f"{scheme}://{request.get_host()}/login"
            message = render_to_string("registration_email.html", {
                "email": email_to, "path": path})
            subject = "Registration confirmation"
            # send_mail(message, [email_to])

            EmailThead([email_to], message, subject).start()

            return Response(data, status=200)
        else:
            return Response(form.errors, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class UserLogin(APIView):
    """
    The user signs in using the email and password used in registation.
    """
    schema = UserLoginSchema()

    def post(self, request):
        # print(request.data)
        form = UserLoginForm(request.data)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data["email"],
                                password=form.cleaned_data["password"])
            if user:
                token = Token.objects.get(user=user).key
                data = UserSerializer(user).data
                data["token"] = token
                return Response(data, status=200)
            return Response({"errors": ["please provide valid credentials"]},
                            status=400)
        # print(form.errors)
        return Response(form.errors, status=400)


# TODO add route for reset password done
# TODO route for initiating a password request - should only receive user email
@method_decorator(csrf_exempt, name='dispatch')
class ResetPasswordView(APIView):
    """
        Creates a new password when the exisiting one is forgotten
    """

    schema = ResetPasswordSchema()

    def post(self, request):
        """
        Request pass word reset by providing an email.
        short code to be used to change password
        short code will be sent to the user which will be used to reset the password
        instead of sending long password reset token generated by django PasswordResetGenerator
        """
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            user = User.objects.filter(
                email=email).first()
            if not user:
                return Response({"email": ["User not found"]}, status=400)
            site = get_current_site(request)
            token = password_reset_token.make_token(user)
            uid64 = urlsafe_base64_encode(force_bytes(user.pk))

            scheme = request.build_absolute_uri().split(":")[0]
            path = f"{scheme}://{request.get_host()}/auth/reset/{uid64}/{token}"
            subject = "Password Reset"
            message = render_to_string('password_reset_mail.html', {
                'user': user,
                "path": path
            })

            EmailThead([email], message, subject).start()

            return Response(
                {"message": f"please check code sent to {email} to change your password",
                 },
                status=200)
        return Response(serializer.errors, status=400)

    @staticmethod
    def gen_token():
        token = ""
        for _ in range(6):
            token += "1234567890"[random.randint(0, 9)]
        return int(token)


@method_decorator(csrf_exempt, name='dispatch')
class ResetPasswordCompleteView(APIView):
    schema = ResetPasswordSchema()

    def get(self, request, uidb64, token):
        # uid64 = request.GET["uid64"]
        # token = request.GET["token"]

        user_id = force_bytes(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=user_id)

        return render(request, "registration/password_reset_confirm.html")

    def post(self, request, uidb64, token):
        """
        Request pass word reset by providing an email.
        short code to be used to change password
        short code will be sent to the user which will be used to reset the password
        instead of sending long password reset token generated by django PasswordResetGenerator
        """

        user_id = force_bytes(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=user_id)

        form = ResetPasswordForm(request.data)
        if form.is_valid():
            user.set_password(form.cleaned_data.get("password1"))

            return render(request, "registration/password_reset_complete.html",
                          {"message": "Your password has been reset"})
        return render(request, "registration/password_reset_confirm.html", {"errors": form.errors})

    @staticmethod
    def gen_token():
        token = ""
        for _ in range(6):
            token += "1234567890"[random.randint(0, 9)]
        return int(token)


@method_decorator(csrf_exempt, name='dispatch')
class UserProfileView(APIView):
    """
    Queries the user details and presents as full profile

    """
    schema = UserSchema()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_object_or_404(User, user=request.user)
        if user:
            data = UserSerializer(user).data

            return Response(data, status=200)
        return Response({"errors": ["User not found"]}, status=400)

    def put(self, request):
        """update profile - email, phone number"""
        form = UserUpdateForm(request.data)

        if form.is_valid():
            user = get_object_or_404(User, token=request.token)

            if form.cleaned_data.get("first_name"):
                user.first_name = form.cleaned_data["first_name"]
                user.save()

            if form.cleaned_data.get("last_name"):
                user.last_name = form.cleaned_data["last_name"]
                user.save()

            if form.cleaned_data.get("email"):
                user.email = form.cleaned_data["email"]
                user.save()

            if form.cleaned_data.get("phone_number"):
                user.phone_number = form.cleaned_data["phone_number"]
                user.save()

            try:
                user.save()

            except:
                print(user)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
