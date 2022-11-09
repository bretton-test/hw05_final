from django.contrib.auth import get_user_model

from .fixtures import get_objects_instances_to_test, PostTest

User = get_user_model()


class PostModelTest(PostTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.another_user = User.objects.create_user(username='IhaveName')
        get_objects_instances_to_test(cls)

    def test_group_have_correct_object_names(self):
        """значение поля group.__str__ совпадает с ожидаемым."""
        self.assertEqual(self.group.title, str(self.group))
