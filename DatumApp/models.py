import datetime
from datetime import datetime

from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save, pre_migrate, pre_save
from django.dispatch import receiver
from django.urls import reverse

# Create your models here.

class Interest(models.Model):

    interest_title = models.CharField(
        max_length=300, 
        null=True)
    is_available = models.BooleanField(
        default=True, 
        null=True)

    class Meta:
        verbose_name = "Interest"
        verbose_name_plural = "Interests"

    def __str__(self):
        return self.interest_title

    def get_absolute_url(self):
        return reverse("interest", kwargs={"pk": self.pk})
    
from datetime import date

class Profile(models.Model):

    male = "Male"
    female = "Female"

    GENDER = [
        (male, "Male"),
        (female, "Female"),
    ]
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        default=None, 
        related_name='user_profile'
        )
    first_name = models.CharField(
        max_length=300, 
        null=True)
    last_name = models.CharField(
        max_length=300, 
        null=True)
    birthdate = models.DateField(
        null=True, 
        help_text='format: YYYY-MM-DD')
    gender = models.CharField(
        max_length=100, 
        null=True, 
        choices=GENDER)
    tg_username = models.CharField(
        max_length=300, 
        null=True, 
        unique=True, 
        help_text='format: @gi_corp'
        )
    interest = models.ManyToManyField(
        Interest, 
        blank=True, 
        related_name='profile_interests'
        )
    photo = models.ImageField(
        upload_to='user_photos/%Y/', 
        null=True, 
        blank=True
        )
    bio = models.TextField(
        max_length=500, 
        null=True
        )
    registered_date = models.DateTimeField(
        default=datetime.now, 
        null=True
        )
    last_update_date = models.DateTimeField(null=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return str(self.tg_username)

    def full_name(self):
        return str(self.first_name + self.last_name)

    def display_interests(self):
        return ', '.join([a.interest_title for a in self.interest.all()])

    def get_age(self):
        return datetime.now().date().year - self.birthdate.year

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})


@receiver(post_save, sender=User)
def profile_post_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        print(f'{instance.username} profile is created.')
        profile = Profile.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            tg_username=instance.username
            )
    else:
        print(f'{instance.username} profile is updated')

# @receiver(pre_save, sender=User)
# def profile_pre_save_receiver(sender, instance, *args, **kwargs):
#     if Profile.objects.get(user=instance):
#         Profile.objects.update(
#             user=instance,
#             last_update_date=datetime.now(),
#             )

import datetime as d

class Preference(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        default=None, 
        related_name='user_preference'
        )
    pref_min_age = models.IntegerField(
        null=True, 
        default=0
        )
    pref_max_age = models.IntegerField(
        null=True, 
        default=0
        )
    
    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("preference", kwargs={"pk": self.pk})

    def get_min_date(self):
        year = datetime.now().date().year - self.pref_min_age
        date = d.datetime(year, 1, 1).date()
        return date
        
    def get_max_date(self):
        year = datetime.now().date().year - self.pref_max_age
        date = d.datetime(year, 1, 1).date()
        return date

@receiver(post_save, sender=User)
def preference_post_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        print(f'{instance.username} preference is created')
        preference = Preference.objects.create(user=instance)
    else:
        print(f'{instance.username} preference is updated')
    

class Match(models.Model):
    current_user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, help_text='current user', 
        related_name='user_match')

    user_requested = models.ForeignKey(
        User, on_delete=models.SET_NULL, 
        null=True, 
        default=None, 
        help_text='whom you liked', 
        related_name='user_match_you')
        
    user_accepted = models.BooleanField(
        default=False, 
        null=True, 
        help_text='if user accepts your match then, this switches to True')

    is_active = models.BooleanField(
        default=True, 
        null=True, 
        help_text='used to remove match connection')

    def __str__(self):
        return str(self.current_user)

    def get_match(self):
        return str(f'{self.current_user} - {self.user_requested}')

    def get_curret_user(self):
        return str(self.current_user)

    def get_user_you_liked(self):
        return str(self.user_requested)

    def get_absolute_url(self):
        return reverse("match", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = 'Matches'
