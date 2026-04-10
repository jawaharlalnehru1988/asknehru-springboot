from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
	usernameOrEmail = serializers.CharField(trim_whitespace=True)
	password = serializers.CharField(trim_whitespace=False)


__all__ = ["LoginSerializer"]
