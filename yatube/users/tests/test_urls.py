from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from .fixtures import get_url_list

User = get_user_model()


class UserURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(UserURLTests.user)

    def test_urls_uses_correct_template_auth(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = get_url_list()
        for address in templates_url_names:
            template, msg_prefix = templates_url_names.get(address)
            with self.subTest(msg=msg_prefix, address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_uses_correct_template_guest(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = get_url_list()
        templates_url_names.pop('/auth/password_change/')
        templates_url_names.pop('/auth/password_change/done/')
        for address in templates_url_names:
            template, msg_prefix = templates_url_names.get(address)
            with self.subTest(msg=msg_prefix, address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
