from django.contrib.auth import get_user_model
from django.urls import reverse

from .fixtures import UrlTest

User = get_user_model()

templates_url_names = {
    '/about/author/': 'about/author.html',
    '/about/tech/': 'about/tech.html',
}
templates_view_names = {
    reverse('about:author'): 'about/author.html',
    reverse('about:tech'): 'about/tech.html',
}


class AboutURLTests(UrlTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="HasNoName")

    def setUp(self):
        self.get_client()

    def test_urls_uses_correct_template_auth(self):
        """URL-адрес использует соответствующий шаблон."""
        self.url_func_test(self.authorized_client, templates_url_names)

    def test_urls_uses_correct_template_guest(self):
        """URL-адрес использует соответствующий шаблон."""
        self.url_func_test(self.client, templates_url_names)

    def test_views_uses_correct_template_auth(self):
        """view адрес использует соответствующий шаблон."""
        self.url_func_test(self.authorized_client, templates_view_names)

    def test_views_uses_correct_template_guest(self):
        """view адрес использует соответствующий шаблон."""
        self.url_func_test(self.client, templates_view_names)
