from django.http import response
from django.test import TestCase, SimpleTestCase, testcases

from datum.models import User, Profile, Preference

class SimpleTests(SimpleTestCase): # SimpleTestCase used to test with no db
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

class PostUserTest(TestCase): # TestCase used to work with db

    # any method that starts with 'test' - django will automatically run when you type in python manage.py test
    
    def setUp(self):
       User.objects.create(username='testuser', password='12345testuser')
    
    def test_user_content(self):
        user = User.objects.get(username='testuser')
        expected_object_name = f'{user.username}'
        self.assertEqual(expected_object_name, 'testuser')

    def test_profile_signal(self):
        profile = Profile.objects.get(user=User.objects.get(username='testuser'))
        if profile:
            return True
        return False

    def test_preference_signal(self):
        preference = Preference.objects.get(user=User.objects.get(username='testuser'))
        if preference:
            return True
        return False
