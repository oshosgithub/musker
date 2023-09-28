from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile

# Register your models here.

#to unregister Group from django-admin page
admin.site.unregister(Group)


#Mix Profile class and User class into one class on admin page. 
class ProfileInline(admin.StackedInline):
        model = Profile

#to show customized User on django-admin page. 
class UserAdmin(admin.ModelAdmin):
        model = User
        fields = ['username',]  #this will show only username on admin page. 
        inlines = [ProfileInline]

#unregister inital User
admin.site.unregister(User)


#register User using customized class UserAdmin
admin.site.register(User, UserAdmin)

