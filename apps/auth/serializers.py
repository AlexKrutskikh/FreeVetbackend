from rest_framework import serializers

from apps.profiles.models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=20)
    photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Profile
        fields = ['name', 'phone', 'photo']


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
