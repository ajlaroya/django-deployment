from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm

# Login
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

def register(request):
    registered = False # check if registered

    if request.method == "POST":
        user_form = UserForm(data=request.POST) # grab info from forms
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() # if valid, grabs data from user form
            user.set_password(user.password) # hash password
            user.save() # saves user to database

            profile = profile_form.save(commit=False) # grabs data from profile form
            profile.user = user

            if 'profile_pic' in request.FILES: # checks pic before saving
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()  # saves profile to database

            registered = True # sets registered to true

        else:
            print(user_form.errors,profile_form.errors) # if invalid print errors

    else: # if request is not POST, sets forms
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password) # authenticates user

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index')) # redirects to homepage

            else:
                return HttpResponse("Account not active!")
        else:
            print("Someone tried to login and failed")
            print(f"Username: {username} and password: {password}")
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request,'basic_app/login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged in, noice!")
