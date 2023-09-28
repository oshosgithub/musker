from django.shortcuts import render, redirect 
from django.contrib import messages 

from .models import Profile

# Create your views here.
def home(request):
    return render(request, 'musker/home.html', {})


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
        return render(request, 'musker/profile.html', {
            'profile': profile,
        })
    else: 
        messages.success(request, 'You must login to see profile....')
        return redirect('home')