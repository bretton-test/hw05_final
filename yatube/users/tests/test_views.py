from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from .fixtures import get_view_list

User = get_user_model()


class UserViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(UserViewsTests.user)

    def test_views_uses_correct_template_auth(self):
        """View-адрес использует соответствующий шаблон."""
        templates_url_names = get_view_list()
        for address in templates_url_names:
            template, msg_prefix = templates_url_names.get(address)
            with self.subTest(msg=msg_prefix, address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_form_based_views(self):
        """form_context contains the required fields"""
        form_fields = {
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'username': forms.fields.CharField,
            'email': forms.fields.EmailField,
            'password1': forms.fields.CharField,
            'password2': forms.fields.CharField,
        }
        response = self.authorized_client.get(reverse('users:signup'))
        for value, expected in form_fields.items():
            form_field = response.context.get('form').fields.get(value)
            self.assertIsInstance(form_field, expected)
