from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.utils.safestring import mark_safe


from .forms import LoginForm, RegistrationForm

# Create your views here.
def auth_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def auth_login(request):
    form = LoginForm(request.POST  or None)
    next_url = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url is not None:
                return HttpResponseRedirect(next_url)
            return HttpResponseRedirect('/')
    context={"form":form}
    return render(request,"login.html",context)

def auth_register(request):
    if request.user.is_authenticated():
        context ={}
    else:
        
        form = RegistrationForm(request.POST  or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            new_user = MyUser()
            new_user.username = username
            email.username = email
            password = form.cleaned_data['password2']
        context = {"form":form}
    return render(request, "accounts/register_form.html",context)