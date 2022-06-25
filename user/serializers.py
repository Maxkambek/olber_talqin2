from rest_framework import serializers
from .models import User, Cargo, VerifyEmail, Work


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
        fields = ('id', 'user', 'title', 'weight', 'price', 'cargo_type', 'status', 'time_when', 'image1', 'distance', 'created')


class CargoAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ('id', 'doer')


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
        fields = ('id', 'username', 'image')


class CargoSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(read_only=True, source="user.username")
    user_rating = serializers.CharField(read_only=True, source="user.rating")
    user_image = serializers.ImageField(read_only=True, source="user.image")
    offers = UserListSerializer(read_only=True, many=True)
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
            'doer',
            'image1',
            'image2',
            'image3',
            'image4',
            'user_name',
            'user_rating',
            'user_image'
        )


class UserDetailSerializer(serializers.ModelSerializer):
    items = CargoListSerializer(required=False, many=True)
    class Meta:
        model = User
        fields = ("username", "email", 'items')


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "user_type")


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'phone',
            'works',
            'telegram',
            'image',
            'rating',
            'user_type',
            'car_type',
            'drive_doc',
            'car_image_1',
            'car_image_2'
            )


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'image', 'account', 'money')


class UserPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('rating',)


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"