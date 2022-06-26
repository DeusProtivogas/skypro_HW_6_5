
from rest_framework import serializers

from user.models import User

from location.models import Location

class EmailValidator:
    def __init__(self, forbidden):
        if not isinstance(forbidden, list):
            forbidden = [forbidden]
        self.forbidden = forbidden

    def __call__(self, value):
        for e_domain in self.forbidden:
            if value.endswith(e_domain) :
                raise serializers.ValidationError(f"Using forbidden email domain name: {e_domain}")

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
    email = serializers.EmailField(validators=[EmailValidator(["rambler.ru"])])

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        user.set_password(validated_data["password"])
        user.save()

        for locations in self._locations:
            obj, _ = Location.objects.get_or_create(name=locations)
            user.locations.add(obj)

        return user

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