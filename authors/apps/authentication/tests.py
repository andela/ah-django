from base64 import b64encode

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import User, UserManager


class UserTestCase(TestCase):
    """ This class defines the test suite for the user model. """

    def setUp(self):
        self.username = "henryjones"
        self.email = "hjones@email.com"
        self.password = "T35ting-i2E"
        self.user = User(
            username=self.username, 
            email=self.email, 
            password=self.password)

    def test_model_can_create_a_user(self):

        previous_count = User.objects.count()
        self.user.save()
        current_count = User.objects.count()

        self.assertNotEqual(previous_count, current_count)
        self.assertEqual(str(self.user), self.email)
    
    
    def test_model_returns_fullname_of_user(self):
        self.user.save()

        self.assertEqual(self.user.get_full_name, self.username)

    def test_model_returns_shortname_of_user(self):
        self.user.save()

        self.assertEqual(self.user.get_short_name(), self.username)
    
class  UserManagerTestCase(TestCase):
    """ This class defines the test suite for the user manager model. """
    
    def setUp(self):
        self.username = "henryjones"
        self.email = "hjones@email.com"
        self.password = "T35ting-i2E"

    def test_manager_can_create_a_regular_user_with_required_fields(self):
        kwargs = {
            "username": self.username,
            "email": self.email,
            "password": self.password}
        
        previous_count = User.objects.count()
        user = User.objects.create_user(**kwargs)
        current_count = User.objects.count()

        self.assertNotEqual(previous_count, current_count)
        self.assertFalse(user.is_superuser)
    
    def test_manager_can_create_a_regular_user_without_password_field(self):
        kwargs = {
            "username": self.username,
            "email": self.email}

        user = User.objects.create_user(**kwargs)
        self.assertIsNotNone(user.password)
        self.assertFalse(user.is_superuser)
    
    def test_manager_cannot_create_a_regular_user_without_username_field(self):
        kwargs = {
            "email": self.email,
            "password": self.password}

        self.assertRaises(TypeError, User.objects.create_user, **kwargs)
    
    def test_manager_cannot_create_a_regular_user_without_email_field(self):
        kwargs = {
            "username": self.username,
            "password": self.password}
        
        self.assertRaises(TypeError, User.objects.create_user, **kwargs)
    
    def test_manager_can_create_a_super_user_with_required_fields(self):
        kwargs = {
            "username": self.username,
            "email": self.email,
            "password": self.password}

        previous_count = User.objects.count()
        user = User.objects.create_superuser(**kwargs)
        current_count = User.objects.count()

        self.assertNotEqual(previous_count, current_count)
        self.assertTrue(user.is_superuser)
    
    def test_manager_cannot_create_a_super_user_without_username_field(self):
        kwargs = {
            "email": self.email,
            "password": self.password}

        self.assertRaises(TypeError, User.objects.create_superuser, **kwargs)
    
    def test_manager_cannot_create_a_super_user_without_email_field(self):
        kwargs = {
            "username": self.username,
            "password": self.password}

        self.assertRaises(TypeError, User.objects.create_superuser, **kwargs)

    def test_manager_cannot_create_a_super_user_without_password_field(self):
        kwargs = {
            "username": self.username,
            "email": self.email}

        self.assertRaises(TypeError, User.objects.create_superuser, **kwargs)
    

class RegistrationAPIViewTestCase(TestCase):
    """ This class defines the test suite for the registration view. """
    
    def setUp(self):
        
        self.existing_user_data= {
            "username": "janejones",
            "email": "jjones@email.com",
            "password": "Enter-123"}

        self.existing_user = User.objects.create_user(**self.existing_user_data)
        self.client = APIClient()
    
    def test_api_can_create_a_user(self):

        user_data = {
            "username": "henryjones",
            "email": "hjones@email.com",
            "password": "Enter-123"}

        response = self.client.post(
            '/api/users/',
            { "user": user_data},
            format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_api_cannot_create_a_user_with_existing_email(self):

        user_data = {
            "username": "peter",
            "email": self.existing_user_data["email"],
            "password": "Enter123"}

        response = self.client.post(
            '/api/users/',
            { "user": user_data},
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user with this email already exists.", response.data["errors"]["email"], )
    
    def test_api_cannot_create_a_user_with_existing_username(self):

        user_data = {
            "username": self.existing_user_data["username"],
            "email": "peter@email.com",
            "password": "Enter123"}

        response = self.client.post(
            '/api/users/',
            { "user": user_data},
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user with this username already exists.", response.data["errors"]["username"])
    
    def test_api_cannot_create_a_user_with_password_lessthan_eight_characters(self):

        user_data = {
            "username": "peter",
            "email": "peter@email.com",
            "password": "Enter"}

        response = self.client.post(
            '/api/users/',
            { "user": user_data},
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Ensure this field has at least 8 characters.", response.data["errors"]["password"])

class LoginAPIViewTestCase(TestCase):
    """ This class defines the test suite for the login view. """

    def setUp(self):

        self.existing_user_data= {
            "username": "janejones",
            "email": "jjones@email.com",
            "password": "Enter-123"}

        self.existing_user = User.objects.create_user(**self.existing_user_data)
        self.client = APIClient()

    def test_api_can_login_a_registered_user(self):

        response = self.client.post(
            '/api/users/login',
            {"user": self.existing_user_data},
            format="json") 

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.existing_user.email, response.data["email"])
    
    def test_api_cannot_login_an_unregistered_user(self):
        user_data = {
            "email": "peter@email.com",
            "password": "Enter-123"}

        response = self.client.post(
            '/api/users/login',
            {"user": user_data},
            format="json") 
     
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'A user with this email and password was not found.',
            response.data["errors"]['error'])

    def test_api_cannot_login_user_with_valid_email_wrong_password_combination(self):
        user_data = {
            "email": self.existing_user.email,
            "password": "enter-123"}  

        response = self.client.post(
            '/api/users/login',
            {"user": user_data},
            format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)      
        self.assertIn(
            'A user with this email and password was not found.',
            response.data["errors"]["error"]
        )

class UserRetrieveUpdateAPIViewTestCase(TestCase):
    """ This class defines the test suite for the view that retrieves and updates a user """
    
    def setUp(self):

        self.existing_user_data= {
            "username": "janejones",
            "email": "jjones@email.com",
            "password": "Enter-123"}

        self.existing_user = User.objects.create_user(**self.existing_user_data)
        self.client = APIClient()
        self.client.login(username="jjones@email.com", password="Enter-123")
    
    def test_api_can_retrieve_a_registered_user(self):

        response = self.client.get(
            '/api/user',
            format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_api_needs_authentication_to_retrieve_a_user(self):

        self.client.logout()

        response = self.client.get(
            '/api/user',
            format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 

    def test_api_can_update_user_data(self):

        new_user_data = {
            "email": "jjones@email.com",
            "bio": "I like eggs for breakfast",
            "image": "https://myimages.com/erwt.png"}

        response = self.client.put(
            '/api/user',
            {"user": new_user_data},
            format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_api_needs_authentication_to_update_user_data(self):
        new_user_data = {
            "email": "jjones@email.com",
            "bio": "I like eggs for breakfast",
            "image": "https://myimages.com/erwt.png"}

        self.client.logout()
        
        response = self.client.put(
            '/api/user',
            {"user": new_user_data},
            format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 
