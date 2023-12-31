from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User

#to crate signal
from django.db.models.signals import post_save

# Create your models here.
class Meep(models.Model):
    user = models.ForeignKey(User, related_name='meeps', on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f'{self.user} '
            f'{self.created_at: %Y-%m-%d %H:%M} '
            f'{self.body}...'
        )
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # above OneToOneField because each user will have only ONE profile. 
    # models.CASCADE means when user will be delated, Profile will also be deleted. 

    follows = models.ManyToManyField('self',
            related_name='followed_by',
            symmetrical=False, #will allow to follow, but that person don't have to follow back. 
            blank=True,
            )
    date_modified = models.DateTimeField(User, auto_now=True)

    def __str__(self):
        return self.user.username


#Creating Profile when new User signs up. 
def create_profile(sender, instance, created, **kwargs):
    if created: 
        user_profile = Profile(user=instance)
        user_profile.save()
        #User will follow himself once a new user crated
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(create_profile, sender=User)

#another way to do signal is using decorators. 
# First: from django.dispatch import receiver
#@receiver(post_save, sender=User) on top of the def create_profile function above.     