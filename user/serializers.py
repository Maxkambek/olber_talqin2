from rest_framework import serializers
from .models import User, Cargo, Car, VerifyEmail


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')


class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyEmail
        fields = '__all__'


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
        fields = ('id', 'user', 'title', 'weight', 'price', 'status', 'when', 'image1', 'distance')


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


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


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'date_joined', 'phone')


class UserDetailSerializer(serializers.ModelSerializer):
    items = CargoListSerializer(required=False, many=True)
    class Meta:
        model = User
        fields = ("username", "email", 'items')