
from http import client
import json
from click import password_option
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
#from rest_framework.test import force_authenticate
from django.contrib.auth.models import User, Group
from .serializers import RegisterSerializer, UserSerializer, GroupSerializer
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import login

# default regiser test case -- register a new user without group
class RegisterTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'email@gmail', 'testpassword')
        self.user.save()
        self.myuser = User.objects.get(username='testuser')
    def test_get_username(self):
        self.assertEquals(self.user.username, 'testuser')
        print('test_get_username completed successfully')

# add group employee and add a user to the group -- user and group create successfully with assigned permissions
# login has token and user info
class AddEmployeeUser(APITestCase):
    def setUp(self):
        # create group employee 
        employee = Group.objects.create(name='employee')
        employee.permissions.add(Permission.objects.get(codename='add_vote'))  
        employee.permissions.add(Permission.objects.get(codename='change_vote'))
        employee.permissions.add(Permission.objects.get(codename='delete_vote'))
        employee.permissions.add(Permission.objects.get(codename='view_restaurant'))
        employee.save()    
        g = Group.objects.get(name='employee')
        self.user = User.objects.create_user('testuser', 'email@gmail', 'testpassword')
        g.user_set.add(self.user)
        self.user.save()
        self.client = APIClient()
        # login setup 
        self.response = self.client.post('/api/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.responseJSON = json.loads(self.response.content)
        self.token = self.responseJSON['token']
    
    def test_api_test_register(self):
        self.assertEqual(self.user.groups.all()[0].name, 'employee')
        self.assertEqual(self.user.username, 'testuser')
        print('register test completed ...')
    
    def test_login_employee(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(self.response.data['username'], 'testuser') # check if user is logged in
        self.assertEqual(self.response.data['type'], 'employee') # check if user is employee    
        self.assertIsNotNone(self.responseJSON['token']) #token has been created
        self.assertEqual(self.responseJSON['token'], self.token) # token response is same as token in login
        print('login test completed ...')
        print('login test returning user completed successfully...')
        print('login test returning token completed successfully...')
        print('login test returning status code successfully...')

    


        
