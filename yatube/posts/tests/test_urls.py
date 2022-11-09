from django.contrib.auth import get_user_model

from .fixtures import (
    TEMPLATE_LIST,
    get_objects_instances_to_test,
    get_url_list,
    PostTest,
)

User = get_user_model()


class PostURLTests(PostTest):
    """Url Pages Tests_Class"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.another_user = User.objects.create_user(username='IhaveName')
        get_objects_instances_to_test(cls)
        get_url_list(cls)

    def setUp(self):
        self.get_client()

    def test_urls_uses_correct_template_auth(self):
        """Тест URL-адреса и шаблона авторизованным пользователем.
        'auth' pattern is expected"""
        interator = 0
        templates_url_names = {}
        for url, test_pattern in self.url_list_with_pattern.items():
            if 'auth' in test_pattern:
                templates_url_names[url] = TEMPLATE_LIST[interator]
            interator += 1
        self.url_func_test(self.authorized_client, templates_url_names)

    def test_urls_uses_correct_template_guest(self):
        """Тест URL-адреса и шаблона пользователем без авторизации.
        'guest' pattern is expected"""
        interator = 0
        templates_url_names = {}
        for url, test_pattern in self.url_list_with_pattern.items():
            if 'guest' in test_pattern:
                templates_url_names[url] = TEMPLATE_LIST[interator]
            interator += 1
        self.url_func_test(self.client, templates_url_names)

    def test_guest_client_404(self):
        """Testing unexisting page for guest_client"""
        response = self.client.get('/unexisting_page/')
        self.assertEqual(response.reason_phrase.upper(), 'NOT FOUND')
        self.assertTemplateUsed(response, 'core/404.html')

    def test_authorized_client_404(self):
        """Testing unexisting page for authorized_client"""
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.reason_phrase.upper(), 'NOT FOUND')
        self.assertTemplateUsed(response, 'core/404.html')

    def test_redirect_anonymous_on_admin_login(self):
        """@login_required page  redirect anonymous to login page.
        url without 'guest' pattern
        """
        for url, test_pattern in self.url_list_with_pattern.items():
            if 'guest' not in test_pattern:
                response = self.client.get(url, follow=True)
                self.assertRedirects(response, f'/auth/login/?next={url}')

    def test_post_edit_redirect_not_author_on_view_post(self):
        """Страница по адресу /post/id/edit/ перенаправит пользователя
        (не автора) на страницу просмотра поста.
        """
        response = self.another_auth_client.get(
            self.page_url['edit_post'], follow=True
        )
        self.assertRedirects(response, self.page_url['post_page'])

    def test_redirect_not_author(self):
        """page with pattern 'author' redirect another user."""
        for url, test_pattern in self.url_list_with_pattern.items():
            if 'author' in test_pattern:
                response = self.another_auth_client.get(url)
                self.assertEqual(response.reason_phrase.upper(), 'FOUND')
