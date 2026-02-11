from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ProductHuntSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(read_only=True)
    image = serializers.ImageField(read_only=True)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token  = super().get_token(user)

        # add extra value
        token["username"] = 'dummy username'
        return token
