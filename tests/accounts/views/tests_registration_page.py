from django.contrib.auth.models import User
from django.test import TestCase


class RegistrationPageTestCase(TestCase):
    def test_invalid_password(self):
        """ Invalid password scenarios. """
        response = self.client.post('/register/', {'username': 'test', 'password1': 'test', 'password2': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="has-error">')
        self.assertContains(response, '<span>The password is too similar to the username.</span>')

        response = self.client.post('/register/', {'username': 'test', 'password1': 'passwor', 'password2': 'passwor'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="has-error">')
        self.assertContains(response, '<span>This password is too short. It must contain at least 8 characters.</span>')

        response = self.client.post('/register/', {'username': 'test', 'password1': 'password',
                                                   'password2': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div class="has-error">')
        self.assertContains(response, '<span>This password is too common.</span>')

    def test_register(self):
        """ Register a user. """
        response = self.client.post('/register/', {'username': 'test', 'password1': 'p@ssw0rd12345',
                                                   'password2': 'p@ssw0rd12345'})
        self.assertRedirects(response, '/login/')
        self.assertEqual(User.objects.filter(username='test').count(), 1)
