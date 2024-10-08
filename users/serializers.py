from rest_framework import serializers
from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=20)

    class Meta:
        model = Profile
        fields = ['name', 'phone']

    def create(self, validated_data):
        # Создаем пользователя
        # username можно задать как номер телефона
        # Создаем профиль и связываем его с пользователем
        profile = Profile.objects.create(
            name=validated_data['name'],
            phone=validated_data['phone']
        )
        return profile


class SMSVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
