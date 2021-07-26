from django.conf import settings  
from django.db.models.signals import post_save 
from django.dispatch import receiver 
from datum.models import Preference, Profile
from django.contrib.auth.models import User

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

@receiver(post_save, sender=User)
def preference_post_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        print(f'{instance.username} preference is created.')
        preference = Preference.objects.create(
            user=instance
            )
    else:
        print(f'{instance.username} preference is updated')