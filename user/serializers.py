from rest_framework import serializers
from .models import User, Cargo, VerifyEmail, Work


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'phone',  'password')


class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyEmail
        fields = '__all__'


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=100)


class ResetSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=100)
    code = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=100)



class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'password')


class CargoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = (
            'user',
            'title',
            'price',
            'weight',
            'from_address',
            'address_from',
            'from_floor',
            'from_kv',
            'to_address',
            'address_to',
            'to_floor',
            'to_kv',
            'time_when',
            'description',
            'cargo_type',
            'doer',
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
        phone = attrs.get('phone')

        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({
                'error': 'Phone number is already registered',
            })

        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create(
            phone=validated_data['phone'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'image', 'rating')


class CargoSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(read_only=True, source="user.username")
    user_rating = serializers.CharField(read_only=True, source="user.rating")
    user_image = serializers.ImageField(read_only=True, source="user.image")
    user_phone = serializers.CharField(read_only=True, source="user.phone")
    offers = UserListSerializer(read_only=True, many=True)
    doer = UserListSerializer(read_only=True, many=False)

    class Meta:
        model = Cargo
        fields = (
            'id',
            'user',
            'title',
            'price',
            'weight',
            'from_address',
            'address_from',
            'from_floor',
            'from_kv',
            'to_address',
            'address_to',
            'to_floor',
            'to_kv',
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
            'user_image',
            'user_phone'
        )


class WorkDetailSerializer(serializers.ModelSerializer):
    offers = UserListSerializer(read_only=True, many=True)
    user = UserListSerializer(required=False, many=False)
    doer = UserListSerializer(required=False, many=False)

    class Meta:
        model = Work
        fields = ('id', 'title', 'user', 'price', 'image', 'status', 'address', 'lat_lon', 'work_time', 'offers', 'description', 'doer')


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"


class WorkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ('id', 'title', 'price', 'image', 'status')


class WorkAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ('id', 'doer')


class UserDetailSerializer(serializers.ModelSerializer):
    workss = WorkListSerializer(required=False, many=True)
    items = CargoListSerializer(required=False, many=True)

    class Meta:
        model = User
        fields = ("username", "phone", 'items', 'workss')


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("phone", "user_type")


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
        fields = ('id', 'rating')
