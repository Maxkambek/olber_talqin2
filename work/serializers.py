from rest_framework import serializers

from user.serializers import UserListSerializer
from work.models import Work


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
        ref_name = 'Work_w'
        model = Work
        fields = ('id', 'title', 'price', 'image', 'status')


class WorkAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ('id', 'doer')
