from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from account.forms import LoginForm

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
