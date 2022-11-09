from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

from .fixtures import PostTest, get_objects_instances_to_test, get_views_list

User = get_user_model()
NUMBER_OF_POSTS = settings.PAGINATION_INTERVAL + 1
NUM_PAGE = 2


class PostPaginatorTests(PostTest):
    """Views with paginator Tests_Class"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="HasNoName")
        cls.another_user = User.objects.create_user(username='IhaveName')
        get_objects_instances_to_test(cls, NUMBER_OF_POSTS)
        get_views_list(cls)

    def setUp(self):
        self.get_client()

    def test_paginator_and_pagination_interval(self):
        """test pagination interval in post_based_views. 'page' pattern"""
        for url, test_pattern in self.page_list_with_pattern.items():
            if 'page' in test_pattern:
                response = self.authorized_client.get(url)
                with self.subTest(url=url):
                    self.assertTrue(
                        isinstance(
                            response.context["page_obj"].paginator, Paginator
                        )
                    )
                    self.assertTrue(
                        len(response.context["page_obj"])
                        == settings.PAGINATION_INTERVAL
                    )

    def test_last_page_contains_correct_amount_records(self):
        """test_pagination in post_based_views. 'page' pattern"""
        for url, test_pattern in self.page_list_with_pattern.items():
            if 'page' in test_pattern:
                url += f"?page={NUM_PAGE}"
                response = self.authorized_client.get(url)
                with self.subTest(url=url):
                    self.assertTrue(
                        len(response.context["page_obj"])
                        == NUMBER_OF_POSTS % settings.PAGINATION_INTERVAL
                    )
