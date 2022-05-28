
from rest_framework import serializers

from user.models import User

from location.models import Location

#
# class LocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Location
#         fields = "__all__"

class UserListSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field="name",
    )

    class Meta:
        model = User
        exclude = ["password"]


class UserDetailSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = User
        fields = "__all__"

class UserCreateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        required=False,
        queryset=Location.objects.all(),
        many=True,
        slug_field="name",
    )

    def is_valid(self, raise_exception=False):
        pass

    class Meta:
        model = User
        fields = "__all__"


class UserUpdateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        queryset=Location.objects.all(),
        many=True,
        slug_field="name",
    )

    class Meta:
        model = User
        fields = "__all__"


class UserDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id"]