from django.test import TestCase


class LoginPageTestCase(TestCase):
    def test_redirect_to_login(self):
        response = self.client.get('', follow=True)
        self.assertRedirects(response, '/login/?next=/')

    def test_invalid_credentials(self):
        response = self.client.post('/login/', {'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<p class="has-error">Invalid username or password</p>')
