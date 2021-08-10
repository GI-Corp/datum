from django.http import response
from django.test import TestCase, SimpleTestCase

<<<<<<< HEAD
class SimpleTests(SimpleTestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
=======
# Create your tests here.

>>>>>>> 4f5bcd5439ce6912781b008a9d58e2e2de0b1a5c
