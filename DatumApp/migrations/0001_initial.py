# Generated by Django 3.2.2 on 2021-07-02 12:16

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interest_title', models.CharField(max_length=300, null=True)),
                ('is_available', models.BooleanField(default=True, null=True)),
            ],
            options={
                'verbose_name': 'Interest',
                'verbose_name_plural': 'Interests',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=300, null=True)),
                ('last_name', models.CharField(max_length=300, null=True)),
                ('birthdate', models.DateField(help_text='format: YYYY-MM-DD', null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=100, null=True)),
                ('tg_username', models.CharField(help_text='format: @gi_corp', max_length=300, null=True, unique=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='user_photos/%Y/')),
                ('bio', models.TextField(max_length=500, null=True)),
                ('registered_date', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('last_update_date', models.DateTimeField(null=True)),
                ('interest', models.ManyToManyField(blank=True, related_name='profile_interests', to='DatumApp.Interest')),
                ('user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pref_min_age', models.IntegerField(null=True)),
                ('pref_max_age', models.IntegerField(null=True)),
                ('user', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_preference', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_accepted', models.BooleanField(default=False, help_text='if user accepts your match then, this switches to True', null=True)),
                ('is_active', models.BooleanField(default=True, help_text='used to remove match connection', null=True)),
                ('current_user', models.ForeignKey(help_text='current user', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_match', to=settings.AUTH_USER_MODEL)),
                ('user_requested', models.ForeignKey(default=None, help_text='whom you liked', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_match_you', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Matches',
            },
        ),
    ]
