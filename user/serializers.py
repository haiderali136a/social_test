from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import UserProfile


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=UserProfile.objects.all())]
    )
    username = serializers.CharField(max_length=50, required=True,
                                     validators=[UniqueValidator(queryset=UserProfile.objects.all())])

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        read_only_fields = ('id', )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True}
        }

    def create(self, validated_data):
        if 'gender' not in validated_data:
            validated_data['gender'] = None
        if 'date_of_birth' not in validated_data:
            validated_data['date_of_birth'] = None
        user = UserProfile.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            gender=validated_data['gender'],
            date_of_birth=validated_data['date_of_birth']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
