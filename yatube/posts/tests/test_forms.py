from django.contrib.auth import get_user_model
from django.db.models import Max

from .fixtures import (
    PostTest,
    get_objects_instances_to_test,
    get_views_list,
    image,
    small_gif,
)
from ..forms import PostForm
from ..models import Group, Post, Comment

User = get_user_model()
TEXT_FOR_POST = 'kuku'
TEXT_FOR_COMMENT = 'test comment'


class PostFormTests(PostTest):
    """Tests for PostForm class"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.another_user = User.objects.create_user(username='IhaveName')
        get_objects_instances_to_test(cls)
        get_views_list(cls)

    def setUp(self):
        self.get_client()

    def last_post_test(self, post_id, post_text, post_author, post_group):
        """Test created or edited post
        Все картинки подбираются родительским классом.
        В папочках как в больнице. тишь да гладь"""
        last_post = Post.objects.first()
        self.assertEqual(last_post.id, post_id)
        self.assertEqual(last_post.text, post_text)
        self.assertEqual(last_post.group, post_group)
        self.assertEqual(last_post.author, post_author)
        self.assertIsNotNone(last_post.image)
        self.assertEqual(last_post.image.read(), small_gif)

    def last_comment_test(
        self,
        last_comment,
        comment_text,
        comment_author,
        comment_post,
    ):
        """Test created comment"""

        self.assertEqual(last_comment.text, comment_text)
        self.assertEqual(last_comment.author, comment_author)
        self.assertEqual(last_comment.post, comment_post)

    def test_post_form_validation_for_blank_items(self):
        """Test post form validation for blank text field"""

        form = PostForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], ['Обязательное поле.'])

    def test_post_form_validation_(self):
        """Test post form validation for existing group"""
        for group in Group.objects.all():
            form = PostForm(data={'text': 'test', 'group': group.slug})
            self.assertTrue(form.is_valid())
        form = PostForm(data={'text': 'test', 'group': ""})
        self.assertTrue(form.is_valid())

    def test_post_form_validation_for_unexisting_slug(self):
        """Test post form validation for unexisting group"""
        form = PostForm(data={'text': 'test', 'group': "3"})
        self.assertFalse(form.is_valid())

    def test_create_post(self):
        """Valid Post_form creates a new Post."""
        data = {
            'text': TEXT_FOR_POST,
            'group': self.group.slug,
            'image': image('my_image.gif'),
        }
        post_count = Post.objects.count()
        response = self.authorized_client.post(
            self.page_url['create_post'],
            data=data,
            follow=True,
            format='multipart',
        )
        self.assertRedirects(response, self.page_url['profile_page'])
        new_post_id = Post.objects.aggregate(Max("id")).get('id__max')
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.last_post_test(new_post_id, TEXT_FOR_POST, self.user, self.group)

    def test_edit_existing_post(self):
        """Valid Post_form edits and saves an existing post"""
        data = {
            'text': TEXT_FOR_POST,
            'group': self.group_two.slug,
            'image': image('my_image1.gif'),
        }
        post_count = Post.objects.count()
        response = self.authorized_client.post(
            self.page_url['edit_post'],
            data=data,
            follow=True,
            format='multipart',
        )
        self.assertRedirects(response, self.page_url['post_page'])
        self.assertEqual(Post.objects.count(), post_count)
        self.last_post_test(
            self.post.id, TEXT_FOR_POST, self.user, self.group_two
        )

    def test_add_comment_to_existing_post(self):
        """comment_form_add_comment_to_existing_post"""
        data = {'text': TEXT_FOR_COMMENT}
        comments_count = self.post.comments.count()
        response = self.authorized_client.post(
            self.page_url['add_comment'], data=data, follow=True
        )
        self.assertRedirects(response, self.page_url['post_page'])
        self.assertEqual(self.post.comments.count(), comments_count + 1)

        self.last_comment_test(
            Comment.objects.first(),
            TEXT_FOR_COMMENT,
            self.user,
            self.post,
        )

        self.last_comment_test(
            response.context["comments"][0],
            TEXT_FOR_COMMENT,
            self.user,
            self.post,
        )
