from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from ..forms import CreationForm

User = get_user_model()


class UserFormsTests(TestCase):

    def test_create_user(self):
        """Valid Post_form creates a new user."""
        data = {
            'first_name': 'a' * 5,
            'last_name': 'b' * 5,
            'username': 'c' * 5,
            'email': 'test@tesc.ru',
            'password1': '!Q2w3e4r',
            'password2': '!Q2w3e4r'
        }
        form = CreationForm(data)
        self.assertTrue(form.is_valid(),
                        msg="Invalid form data")
        user_count = User.objects.count()
        response = self.client.post(
            reverse('users:signup'),
            data=data,
            follow=True)
        self.assertRedirects(response,
                             reverse_lazy('posts:index'))
        self.assertEqual(User.objects.count(), user_count + 1)
