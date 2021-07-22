from django.shortcuts import render, redirect
from .forms import *
from.forms import LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def login_signup_page(request):
    return render(request,'base.html')
def about_page(request):
    return render(request,'about.html')
def register_page(request):
    title = 'Register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print('Hovi giyo')
            response = redirect("login")
            return response
        else:
            print('Koni hoyo!')
    context={
        'title':title,
        'form':form,
    }
    return render(request,'register.html',context)

def login_page(request):
    form = LoginForm()
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/ques')#redirect it to home of posts
        else:
            messages.info(request, "Username OR Password is incorrect.")
    context={'form':form}
    return render(request,'login.html',context)

def logout_page(request):
    logout(request)
    print('Logged Out')
    return render(request, 'base.html')
