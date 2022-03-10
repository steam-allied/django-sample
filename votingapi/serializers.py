#Serializer for converting complex objects into native Python datatypes and deserialize parsed data back into complex types

from rest_framework import serializers
from votingapi.models import Restaurant,Menu,Vote
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model=Restaurant
        fields=('restaurantId','restaurantName','restaurantAddress','userId')

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model=Menu
        fields=('menutId','menuName','menuDescription','restaurantId','menuDate')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vote
        fields=('voteId','voteMenuId','userId','voteMenuDate' , 'rate')

class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('name',)

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_type = self.context['request'].data.get('type')
        user_password = self.context['request'].data.get('password')
        try:
            validate_password(user_password)
        except:
            raise serializers.ValidationError("Password is not valid")
        
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        g = Group.objects.get(name=user_type)
        g.user_set.add(user)
        return user

