from datetime import timezone
from django.utils.timezone import datetime, now
# вместо datetime использовать timezone, datetime не учитывает настройки django
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.

class Interest(models.Model):

    interest_title = models.CharField(
        max_length=300, 
        null=True, 
        unique=True
        )
    is_available = models.BooleanField(
        default=True)

    class Meta:
        verbose_name = "Interest"
        verbose_name_plural = "Interests"

    def __str__(self):
        return self.interest_title

    def get_absolute_url(self):
        return reverse("interest/", kwargs={"pk": self.pk})

class Profile(models.Model):

    male = "Male"
    female = "Female"

    GENDERS = [
        (male, "Male"),
        (female, "Female"),
    ]
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        default=None, 
        related_name='profile'
        )
    first_name = models.CharField(
        max_length=300, 
        null=True
        )
    last_name = models.CharField(
        max_length=300, 
        null=True
        )
    birthdate = models.DateField(
        null=True, 
        help_text='format: YYYY-MM-DD'
        )
    gender = models.CharField(
        max_length=100, 
        null=True, 
        choices=GENDERS
        )
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
        default= datetime.now(), 
        )
    last_update_date = models.DateTimeField(
        null=True, 
        auto_now=True
        )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return str(self.tg_username)

    def full_name(self):
        return str(f'{self.first_name} {self.last_name}')

    def display_interests(self):
        return ', '.join([a.interest_title for a in self.interest.all()])

    def get_age(self):
        return datetime.now().date().year - self.birthdate.year

    def get_absolute_url(self):
        return reverse("profile/", kwargs={"pk": self.pk})

class Preference(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        default=None, 
        related_name='user_preference'
        )
    pref_min_age = models.IntegerField(
        default=0
        )
    pref_max_age = models.IntegerField(
        default=0
        )
    
    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("preference", kwargs={"pk": self.pk})

    def get_min_date(self):
        year = datetime.now().date().year - self.pref_min_age
        date = datetime(year, 1, 1).date()
        return date
        
    def get_max_date(self):
        year = datetime.now().date().year - self.pref_max_age
        date = datetime(year, 1, 1).date()
        return date

class Match(models.Model):
    current_user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        help_text='current user', 
        related_name='user_match'
        )

    user_requested = models.ForeignKey(
        User, on_delete=models.SET_NULL, 
        null=True,
        default=None, 
        help_text='whom you liked', 
        related_name='user_match_you'
        )
        
    user_accepted = models.BooleanField(
        default=False, 
        help_text='if user accepts your match then, this switches to True'
        )

    is_active = models.BooleanField(
        default=True, 
        help_text='used to remove match connection'
        )

    def __str__(self):
        return str(self.current_user)

    def get_match(self):
        return str(f'{self.current_user} - {self.user_requested}')

    def get_curret_user(self):
        return str(self.current_user)

    def get_user_you_liked(self):
        return str(self.user_requested)

    def get_absolute_url(self):
        return reverse("match/", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = 'Matches'
