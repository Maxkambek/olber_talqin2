from rest_framework import serializers
from cargo.models import Cargo
from user.models import User


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        ref_name = 'User_c'
        model = User
        fields = ('id', 'username', 'image', 'rating')


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
