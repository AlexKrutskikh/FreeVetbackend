from rest_framework import serializers
from .models import Profile

"""Create JSON for Twilio"""

class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=20)

    class Meta:
        model = Profile
        fields = ['name', 'phone']

    def create(self, validated_data):
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