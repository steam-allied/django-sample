
from bdb import set_trace
from email import header
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
        self.user = User.objects.create_user(
            'testuser', 'email@gmail', 'testpassword')
        self.user.save()
        self.myuser = User.objects.get(username='testuser')

    def test_get_username(self):
        self.assertEquals(self.user.username, 'testuser')
        print('test_get_username completed successfully')

# add group employee and add a user to the group -- user and group create successfully with assigned permissions
# login has token and user info


class EmployeeUser(APITestCase):
    def setUp(self):
        # create group employee
        employee = Group.objects.create(name='employee')
        employee.permissions.add(Permission.objects.get(codename='add_vote'))
        employee.permissions.add(
            Permission.objects.get(codename='change_vote'))
        employee.permissions.add(
            Permission.objects.get(codename='delete_vote'))
        employee.permissions.add(
            Permission.objects.get(codename='view_restaurant'))

        employee.save()
        g = Group.objects.get(name='employee')
        self.user = User.objects.create_user(
            'testuser', 'email@gmail', 'testpassword')
        g.user_set.add(self.user)
        self.user.save()
        self.client = APIClient()
        # login setup
        self.response = self.client.post(
            '/api/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.responseJSON = json.loads(self.response.content)
        self.token = self.responseJSON['token']

        self.client1 = APIClient()
        self.client1.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        #self.client1.header(HTTP_ACCEPT='application/json;version=1.0')

        self.vote_response = self.client1.post(
            '/api/vote/', {'voteMenuId': 29, 'voteMenuDate': '2019-10-10'})
        print('setup **********************************************************')
        print(self.vote_response)
        self.responseJSON_vote = json.loads(
            self.vote_response.content)

    def test_api_test_register(self):
        self.assertEqual(self.user.groups.all()[0].name, 'employee')
        self.assertEqual(self.user.username, 'testuser')
        print('register test completed ...')

    def test_login_employee(self):
        self.assertEqual(self.response.status_code, 200)
        # check if user is logged in
        self.assertEqual(self.response.data['username'], 'testuser')
        # check if user is employee
        self.assertEqual(self.response.data['type'], 'employee')
        # token has been created
        self.assertIsNotNone(self.responseJSON['token'])
        # token response is same as token in login
        self.assertEqual(self.responseJSON['token'], self.token)
        print('login test completed ...')
        print('login test returning user completed successfully...')
        print('login test returning token completed successfully...')
        print('login test returning status code successfully...')

    def test_create_vote(self):
        # create vote
        self.assertEqual(self.vote_response.status_code, 200)
        print('create vote test completed successfully...')


class RestaurantUser(APITestCase):
    def setUp(self):
        # create group restaurant
        restaurant = Group.objects.create(name='restaurant')
        restaurant.permissions.add(Permission.objects.get(codename='add_menu'))
        restaurant.permissions.add(
            Permission.objects.get(codename='change_menu'))
        restaurant.permissions.add(
            Permission.objects.get(codename='delete_menu'))
        restaurant.permissions.add(
            Permission.objects.get(codename='view_menu'))
        restaurant.permissions.add(
            Permission.objects.get(codename='add_restaurant'))
        restaurant.permissions.add(
            Permission.objects.get(codename='change_restaurant'))
        restaurant.permissions.add(
            Permission.objects.get(codename='view_restaurant'))

        restaurant.save()
        g = Group.objects.get(name='restaurant')
        self.user = User.objects.create_user(
            'testuser-rest', 'email@gmail', 'testpassword')
        g.user_set.add(self.user)
        self.user.save()
        self.client = APIClient()
        # login setup
        self.response = self.client.post(
            '/api/login/', {'username': 'testuser-rest', 'password': 'testpassword'})
        self.responseJSON = json.loads(self.response.content)
        self.token = self.responseJSON['token']

        # create Restaurant setup
        self.client1 = APIClient()
        self.client1.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.response_restaurant = self.client1.post(
            '/api/restaurant', {'restaurantName': 'test restaurant', 'restaurantAddress': 'test address'}, format='json')
        print(self.token)
        print(self.response_restaurant)
        self.responseJSON_restaurant = json.loads(
            self.response_restaurant.content)

        # restaurant list setup
        self.client2 = APIClient()
        self.client2.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        self.response_restaurant_list = self.client2.get(
            '/api/restaurant')

        # self.response_restaurant_list = json.loads(
        #     self.response_restaurant_list.content)

    def test_api_test_register(self):
        self.assertEqual(self.user.groups.all()[0].name, 'restaurant')
        self.assertEqual(self.user.username, 'testuser-rest')
        print('register test completed ...')

    def test_login_employee(self):
        self.assertEqual(self.response.status_code, 200)
        # check if user is logged in
        self.assertEqual(self.response.data['username'], 'testuser-rest')
        # check if user is employee
        self.assertEqual(self.response.data['type'], 'restaurant')
        # token has been created
        self.assertIsNotNone(self.responseJSON['token'])
        # token response is same as token in login
        self.assertEqual(self.responseJSON['token'], self.token)
        print('login test completed ...')
        print('login test returning user completed successfully...')
        print('login test returning token completed successfully...')
        print('login test returning status code successfully...')

    def test_create_restaurant(self):
        # create restaurant
        self.assertEqual(self.response_restaurant.status_code, 200)
        self.assertIsNotNone(self.responseJSON_restaurant['restaurantName'])
        self.assertIsNotNone(self.responseJSON_restaurant['restaurantAddress'])
        print('create restaurant test completed successfully...')

    def test_get_restaurant_list(self):
        self.assertEqual(self.response_restaurant_list.status_code, 200)
        self.assertEqual(len(self.response_restaurant_list.data), 1)
