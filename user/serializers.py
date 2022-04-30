from rest_framework import serializers
from .models import User, Cargo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate(self, attrs):
        email = attrs.get('email')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                'error': 'Email is already registered',
            })

        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],

        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'


class CargoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ('id', 'title', 'weight', 'price', 'status', 'when', 'image1')