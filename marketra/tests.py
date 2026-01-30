from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticationTests(TestCase):
    def test_signup_page_status_code(self):
        response = self.client.get(reverse('marketra:signup'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_status_code(self):
        response = self.client.get(reverse('marketra:login'))
        self.assertEqual(response.status_code, 200)


    def test_user_signup_logic(self):
        response = self.client.post(reverse('marketra:signup'), {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='testuser').exists())
