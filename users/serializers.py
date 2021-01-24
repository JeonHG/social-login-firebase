from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User

# from core.serializers import RelatedShelfSerializer


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "avatar",
            "first_name",
            "last_name",
            "email",
        )
        read_only_fields = ("id",)

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validated_data):
        password = validated_data.get("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.save()
        return instance

    # def validate_first_name(self, value):
    #     return value.upper()