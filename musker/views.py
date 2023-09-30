from django.shortcuts import render, redirect 
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, Meep
from .forms import MeepForm, RegisterForm


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        meeps = Meep.objects.all().order_by('-created_at')
        form = MeepForm()
        if request.method=='POST':
            form = MeepForm(request.POST or None)
            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = request.user
                meep.save()
                form = MeepForm()
                messages.success(request, ('Your meep posted!'))
        return render(request, 'musker/home.html', {
            'meeps': meeps, 
            'form': form, 
        })
    else:
        meeps = Meep.objects.all().order_by('-created_at')
        return render(request, 'musker/home.html', {
            'meeps':meeps,
        })

def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST or None)
        if form.is_valid:
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            messages.success(request, f"Registration created!")
            return redirect ('home')
    return render(request, 'musker/register.html',{
        'form': form, 
    })

def update_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        form = RegisterForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request,'Your profile updated.')
            return redirect('home')
        return render(request, 'musker/update_profile.html',{'form':form})
    else:
        messages.success(request,'You must log in to update')
        return redirect('home')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back {user.username.capitalize()}')
            return redirect('home')
    return render(request, 'musker/login.html',{

    })

def logout_user(request):
    logout(request)
    return redirect ('home')

def profile_list(request):
    if request.user.is_authenticated:
    #this will bring all objects except the user requesting. 
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'musker/profile_list.html', {
            'profiles': profiles,
        })
    else: 
        messages.success(request, 'You must login to see this page...')
        return redirect('home')

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        meeps = Meep.objects.filter(user_id=pk)

        #POST form logic for follow/unfollow
        if request.method == 'POST':
            #get the current user
            current_user_profile = request.user.profile
            #get form data
            action = request.POST['follow']
            #decide to follow or unfollow
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()

        return render(request, 'musker/profile.html', {
            'profile': profile,
            'meeps': meeps,
        })
    else: 
        messages.success(request, 'You must login to see profile....')
        return redirect('home')