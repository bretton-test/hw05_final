from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase

User = get_user_model()


class UrlTest(TestCase):
    """Class to test url and template parameters"""

    authorized_client: Client
    user = None

    def url_func_test(self, client, templates_url_names):
        """test url and html_template"""
        for address, template in templates_url_names.items():
            with self.subTest(self, address=address):
                response = client.get(address)
                self.assertEqual(response.reason_phrase.upper(), 'OK')
                self.assertTemplateUsed(response, template)

    def get_client(self):
        """Returns a client instance"""
        if self.user:
            self.authorized_client = Client()
            self.authorized_client.force_login(self.user)
