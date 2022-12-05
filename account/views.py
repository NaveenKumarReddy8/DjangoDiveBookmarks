from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from account.forms import LoginForm, ProfileEditForm, UserEditForm, UserRegistration
from account.models import Profile

# Create your views here.


def user_login(request: HttpRequest):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user:
                if user.is_active:
                    return HttpResponse("Authentication Successful")
                return HttpResponse("Disabled account")
            return HttpResponse("Invalid Login")
    form = LoginForm()
    return render(
        request=request, template_name="account/login.html", context={"form": form}
    )


@login_required
def dashboard(request: HttpRequest):
    return render(
        request=request,
        template_name="account/dashboard.html",
        context={"section": "dashboard"},
    )


def register(request: HttpRequest):
    if request.method == "POST":
        user_form = UserRegistration(request.POST)
        if user_form.is_valid():
            new_user: User = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(
                request=request,
                template_name="account/register_done.html",
                context={"new_user": new_user},
            )
    else:
        user_form = UserRegistration()
    return render(
        request=request,
        template_name="account/register.html",
        context={"user_form": user_form},
    )


@login_required
def edit(request: HttpRequest):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if all((user_form.is_valid(), profile_form.is_valid())):
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request=request,
        template_name="account/edit.html",
        context={"user_form": user_form, "profile_form": profile_form},
    )
