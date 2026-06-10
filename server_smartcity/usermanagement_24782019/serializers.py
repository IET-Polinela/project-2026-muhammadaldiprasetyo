from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        # Menggunakan field bawaan AbstractUser Django
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Menggunakan create_user agar password otomatis di-hashing di database
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user