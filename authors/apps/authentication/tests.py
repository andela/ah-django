from django.test import TestCase
from .models import User, UserManager


class UserModelTestCase(TestCase):
    """ This class defines the test suite for the user model. """

    def setUp(self):
        self.username = "henryjones"
        self.email = "hjones@email.com"
        self.password = "T35ting-i2E"
        self.user = User(username=self.username, email=self.email, password=self.password)

    def test_model_can_create_a_user(self):
        fields = [
            self.username,
            self.email,
            self.password
        ]

        previous_count = User.objects.count()
        self.user.save()
        current_count = User.objects.count()

        self.assertNotEqual(previous_count, current_count)
        self.assertIn(self.user.username, fields)
        self.assertIn(self.user.email, fields)
        self.assertIn(self.user.password, fields)
    
class  UserManagerTestCase(TestCase):
    """ This class defines the test suite for the user manager model. """
    
    def setUp(self):
        self.username = "henryjones"
        self.email = "hjones@email.com"
        self.password = "T35ting-i2E"

    def test_manager_can_create_a_regular_user_with_required_fields(self):
        previous_count = User.objects.count()
        user = User.objects.create_user(username=self.username, email=self.email, password=self.password)
        current_count = User.objects.count()

        self.assertNotEqual(previous_count, current_count)
    
    def test_manager_cannot_create_a_regular_user_without_required_fields(self):

        self.assertRaises(TypeError, User.objects.create_user)
    
    def test_manager_can_create_a_super_user_with_required_fields(self):
        previous_count = User.objects.count()
        user = User.objects.create_superuser(username=self.username, email=self.email, password=self.password)
        current_count = User.objects.count()

        self.assertNotEqual(previous_count, current_count)
    
    def test_manager_cannot_create_a_super_user_without_required_fields(self):
        
        self.assertRaises(TypeError, User.objects.create_superuser)
        