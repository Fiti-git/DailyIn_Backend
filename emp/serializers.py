from rest_framework import serializers
from django.contrib.auth.models import User
from .models import EmployeeProfile , Outlet


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user

class EmployeeProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = EmployeeProfile
        fields = ['id', 'user', 'first_name', 'last_name', 'emp_code', 'contact_number', 'outlet']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        employee = EmployeeProfile.objects.create(user=user, **validated_data)
        return employee
    
class OutletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outlet
        fields = ['id', 'name', 'address']

class EmployeeProfileReadOnlySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # or customize to show username/email
    outlet = serializers.CharField(source='outlet.name')  # show outlet name

    class Meta:
        model = EmployeeProfile
        fields = ['id', 'user', 'first_name', 'last_name', 'emp_code', 'contact_number', 'outlet']