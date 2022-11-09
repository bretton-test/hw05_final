from django import forms
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import QuerySet
from django.urls import reverse

from .fixtures import (
    TEMPLATE_LIST,
    get_objects_instances_to_test,
    get_views_list,
    PostTest,
)
from ..forms import PostForm, CommentForm
from ..models import Post, Follow

User = get_user_model()


class PostPagesTests(PostTest):
    """Views pages Tests_Class"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="HasNoName")
        cls.another_user = User.objects.create_user(username='IhaveName')
        get_objects_instances_to_test(cls)
        get_views_list(cls)

    def setUp(self):
        self.get_client()
        cache.clear()

    def context_post_test(self, post_to_test):
        """Test post object"""
        self.assertEqual(post_to_test.group, self.post.group)
        self.assertEqual(post_to_test.text, self.post.text)
        self.assertEqual(post_to_test.author, self.post.author)
        self.assertEqual(post_to_test.id, self.post.id)
        self.assertEqual(post_to_test.image, self.post.image)

    def response_view_test(self, response, context_attributes, form_fields):
        for value, expected in context_attributes.items():
            context_atr = response.context.get(value)
            self.assertIsInstance(context_atr, expected)
        for value, expected in form_fields.items():
            form_field = response.context.get("form").fields.get(value)
            self.assertIsInstance(form_field, expected)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = dict(
            zip(self.page_list_with_pattern.keys(), TEMPLATE_LIST)
        )

        self.url_func_test(self.authorized_client, templates_url_names)

    def test_post_based_views(self):
        """test context for post_based views with paginator. 'page' pattern"""
        for url, test_pattern in self.page_list_with_pattern.items():
            if 'page' in test_pattern:
                response = self.authorized_client.get(url)
                with self.subTest(url=url):
                    self.context_post_test(response.context["page_obj"][0])

    def test_post_detail_views(self):
        """test_post_detail_views. 'post' pattern"""
        for url, test_pattern in self.page_list_with_pattern.items():
            if test_pattern == ['post']:
                response = self.authorized_client.get(url)
                with self.assertRaises(TypeError, msg="post is not object."):
                    response.context["post"][0]
                self.context_post_test(response.context["post"])

    def test_post_from_another_group(self):
        """test_post_from_another_group"""
        response = self.authorized_client.get(self.page_url["group_page"])
        post_one = response.context["page_obj"][0]
        post_two = Post.objects.filter(group=self.group_two).first()
        self.assertNotEqual(
            post_one, post_two, msg="post in another group page"
        )
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group_two.slug})
        )
        self.assertNotContains(response, self.post)
        self.assertTrue(len(response.context["page_obj"]) == 0)

    def test_form_based_views(self):
        """form_context contains the required fields. 'form' pattern"""
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.models.ModelChoiceField,
        }
        context_attributes = {"form": PostForm, "is_edit": bool}

        for url, test_pattern in self.page_list_with_pattern.items():
            if 'form' in test_pattern:
                response = self.authorized_client.get(url)
                self.response_view_test(
                    response, context_attributes, form_fields
                )

    def test_create_post_view(self):
        """test_create_post_is_edit_attribute"""
        response = self.authorized_client.get(self.page_url["create_post"])
        self.assertFalse(response.context.get("is_edit"))

    def test_edit_post_view(self):
        """test_edit_post_is_edit_attribute"""
        response = self.authorized_client.get(self.page_url["edit_post"])
        self.assertTrue(response.context.get("is_edit"))

    def test_comment_based_views(self):
        """form_context contains the required fields. 'comment' pattern"""
        form_fields = {
            "text": forms.fields.CharField,
        }
        context_attributes = {"form": CommentForm, "comments": QuerySet}

        for url, test_pattern in self.page_list_with_pattern.items():
            if 'comment' in test_pattern:
                response = self.authorized_client.get(url)
                self.response_view_test(
                    response, context_attributes, form_fields
                )

    def test_follow_view(self):
        """test follow functionality"""
        Follow.objects.all().delete()
        self.another_auth_client.get(self.page_url["follow"])
        self.assertEqual(Follow.objects.count(), 1, 'подписка не добавилась')
        self.another_auth_client.get(self.page_url["follow"])
        self.assertEqual(
            Follow.objects.count(), 1, 'вторая подписка добавилась'
        )
        self.authorized_client.get(self.page_url["follow"])
        self.assertEqual(
            Follow.objects.count(), 1, 'подписка на себя добавилась'
        )
        response = self.another_auth_client.get(self.page_url["follow_page"])
        post_one = response.context["page_obj"][0]
        self.context_post_test(post_one)
        response = self.authorized_client.get(self.page_url["follow_page"])
        self.assertNotContains(response, self.post)

    def test_unfollow_view(self):
        """test unfollow functionality"""
        self.authorized_client.get(self.page_url["unfollow"])
        self.assertEqual(Follow.objects.count(), 1, 'сам от себя отписался')
        Follow.objects.all().delete()
        self.another_auth_client.get(self.page_url["follow"])
        self.another_auth_client.get(self.page_url["unfollow"])
        self.assertEqual(Follow.objects.count(), 0, 'подписка не удалилась')

    def test_cached_main_page(self):
        """test  cache for the main page"""
        response_one = self.authorized_client.get(self.page_url["main_page"])
        Post.objects.all().delete()
        response_two = self.authorized_client.get(self.page_url["main_page"])
        self.assertEqual(response_one.content, response_two.content)
        cache.clear()
        response_three = self.authorized_client.get(self.page_url["main_page"])
        self.assertNotEqual(response_one.content, response_three.content)
