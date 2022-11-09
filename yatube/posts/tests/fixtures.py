import shutil
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse

from ..models import Group, Post, Follow

TEMPLATE_LIST = [
    ('posts/index.html', 'index page test'),
    ('posts/group_list.html', 'group_list page test'),
    ('posts/profile.html', 'profile page test'),
    ('posts/post_detail.html', 'posts_detail page test'),
    ('posts/create_post.html', 'post_edit page test'),
    ('posts/create_post.html', 'post_create page test'),
    ('', ''),
    ('posts/follow.html', 'follow page test'),
    ('', ''),
    ('', ''),
]

URL_LIST = [
    'main_page',
    'group_page',
    'profile_page',
    'post_page',
    'edit_post',
    'create_post',
    'add_comment',
    'follow_page',
    'follow',
    'unfollow',
]

TEST_PATTERN_VIEWS = [
    ['post', 'page'],
    ['post', 'page'],
    ['post', 'page'],
    ['post', 'comment'],
    ['form'],
    ['form'],
    [],
    ['post', 'page'],
    [],
    [],
]

TEST_PATTERN_URLS = [
    ['auth', 'guest'],
    ['auth', 'guest'],
    ['auth', 'guest'],
    ['auth', 'guest'],
    ['auth', 'author'],
    ['auth'],
    ['comment'],
    ['auth'],
    ['follow'],
    ['follow'],
]

small_gif = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00'
    b'\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
    b'\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


def image(image_name: str):
    """Return small in memory image"""
    return SimpleUploadedFile(
        name=image_name, content=small_gif, content_type='image/gif'
    )


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostTest(TestCase):
    """Class to test post creation and editing"""

    authorized_client: Client
    another_auth_client: Client
    user = None
    another_user = None

    def url_func_test(self, client, templates_url_names):
        """test url and html_template"""
        for address in templates_url_names:
            template, msg_prefix = templates_url_names.get(address)
            if template:
                with self.subTest(msg=msg_prefix, address=address):
                    response = client.get(address)
                    self.assertEqual(response.reason_phrase.upper(), 'OK')
                    self.assertTemplateUsed(response, template)

    def get_client(self):
        """Returns a client instance"""
        if self.user:
            self.authorized_client = Client()
            self.authorized_client.force_login(self.user)
        if self.another_user:
            self.another_auth_client = Client()
            self.another_auth_client.force_login(self.another_user)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)


def get_objects_instances_to_test(cls, number_of_posts=1):
    """create test data objects"""
    cls.group = Group.objects.create(
        title='Тестовая группа 1',
        slug=1,
        description='Тестовое описание группы',
    )
    cls.group_two = Group.objects.create(
        title='Тестовая группа 2',
        slug=2,
        description='Тестовое описание группы',
    )
    test_image = SimpleUploadedFile(
        name='small.gif', content=small_gif, content_type='image/gif'
    )

    Post.objects.bulk_create(
        [
            Post(
                author=cls.user,
                text=f'Тестовый пост {post_num}',
                group=cls.group,
                image=test_image,
            )
            for post_num in range(number_of_posts)
        ]
    )
    cls.post = Post.objects.first()

    Follow.objects.create(user=cls.user, author=cls.user)


def get_views_list(test_case_object):
    """Create url_list from views_list and exists objects.
    Called from setUpClass method TestCase object
    """
    posts_views_list = [
        reverse('posts:index'),
        reverse(
            'posts:group_list', kwargs={'slug': test_case_object.group.slug}
        ),
        reverse(
            'posts:profile',
            kwargs={'username': test_case_object.user.username},
        ),
        reverse(
            'posts:post_detail', kwargs={'post_id': test_case_object.post.id}
        ),
        reverse(
            'posts:post_edit', kwargs={'post_id': test_case_object.post.id}
        ),
        reverse('posts:post_create'),
        reverse(
            'posts:add_comment', kwargs={'post_id': test_case_object.post.id}
        ),
        reverse('posts:follow_index'),
        reverse(
            'posts:profile_follow',
            kwargs={'username': test_case_object.user.username},
        ),
        reverse(
            'posts:profile_unfollow',
            kwargs={'username': test_case_object.user.username},
        ),
    ]
    test_case_object.page_list_with_pattern = dict(
        zip(posts_views_list, TEST_PATTERN_VIEWS)
    )
    test_case_object.page_url = dict(zip(URL_LIST, posts_views_list))


def get_url_list(test_case_object):
    """Create url_list from url and exists objects
    Called from setUpClass method TestCase object
    """
    posts_url_list = [
        '/',
        f'/group/{test_case_object.group.slug}/',
        f'/profile/{test_case_object.user.username}/',
        f'/posts/{test_case_object.post.id}/',
        f'/posts/{test_case_object.post.id}/edit/',
        '/create/',
        f'/posts/{test_case_object.post.id}/comment/',
        '/follow/',
        f'/profile/{test_case_object.user.username}/follow/',
        f'/profile/{test_case_object.user.username}/unfollow/',
    ]
    test_case_object.url_list_with_pattern = dict(
        zip(posts_url_list, TEST_PATTERN_URLS)
    )
    test_case_object.page_url = dict(zip(URL_LIST, posts_url_list))
