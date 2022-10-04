from rest_framework import serializers

from cargo.serializers import CargoListSerializer
from work.models import Work
from .models import User, VerifyEmail


class WorkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ('id', 'title', 'price', 'image', 'status')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone',)


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
            'car_image_2',
            'car_number',
            )


class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'works',
            'telegram',
            'image',
            'rating',
            'user_type',
            'car_type',
            'drive_doc',
            'car_image_1',
            'car_image_2',
            'car_number',
            )


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'image', 'account', 'money')


class UserCashSerializer(serializers.Serializer):
    account_id = serializers.CharField(max_length=7)
    amount = serializers.CharField(max_length=15)


class UserPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'rating')


class AddressSerializer(serializers.Serializer):
    lat = serializers.CharField(max_length=50)
    lng = serializers.CharField(max_length=50)


