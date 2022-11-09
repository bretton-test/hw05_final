from django.contrib.auth import get_user_model

from .fixtures import get_objects_instances_to_test, PostTest

User = get_user_model()
POST_NAME_LENGTH = 15


class PostModelTest(PostTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.another_user = User.objects.create_user(username='IhaveName')
        get_objects_instances_to_test(cls)

    def test_post_have_correct_object_names(self):
        """значение поля post.__str__ совпадает с ожидаемым."""
        self.assertEqual(self.post.text[:POST_NAME_LENGTH], str(self.post))

    def test_verbose_name(self):
        """verbose_name в полях Post совпадает с ожидаемым."""
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Сообщество',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).verbose_name,
                    expected_value,
                )

    def test_help_text(self):
        """help_text в полях Post совпадает с ожидаемым."""
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Сообщество, к которому будет относиться пост',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).help_text, expected_value
                )
