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
    user_name = serializers.CharField(read_only=True, source="user.username")
    user_rating = serializers.CharField(read_only=True, source="user.rating")
    user_image = serializers.CharField(read_only=True, source="user.image")

    class Meta:
        model = Cargo
        fields = (
            'id',
            'user',
            'title',
            'price',
            'weight',
            'from_address',
            'from_floor',
            'from_kv',
            'from_persons',
            'to_address',
            'to_floor',
            'to_kv',
            'to_persons',
            'time_when',
            'description',
            'cargo_type',
            'distance',
            'offers',
            'image1',
            'image2',
            'image3',
            'image4',
            'user_name',
            'user_rating',
            'user_image'
        )


class CargoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = (
            'user',
            'title',
            'price',
            'weight',
            'from_address',
            'from_floor',
            'from_kv',
            'from_persons',
            'to_address',
            'to_floor',
            'to_kv',
            'to_persons',
            'time_when',
            'description',
            'cargo_type',
            'image1',
            'image2',
            'image3',
            'image4'
        )


class CargoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ('id', 'user', 'title', 'weight', 'price', 'cargo_type', 'status', 'time_when', 'image1', 'distance')


class CargoAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ('id', 'doer')


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):

    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


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


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", 'username', 'first_name', 'last_name', 'phone', 'works', 'telegram', 'user_type', 'image', 'rating')
