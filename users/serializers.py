from django.contrib.auth.models import User
from rest_framework import serializers


class UserCreateSerializer(serializers.Serializer):
	username = serializers.CharField(min_length=3, max_length=50, trim_whitespace=True)
	email = serializers.EmailField(max_length=254)
	password = serializers.CharField(min_length=6, max_length=72, trim_whitespace=False)

	def validate_username(self, value):
		if User.objects.filter(username__iexact=value).exists():
			raise serializers.ValidationError("Username already exists.")
		return value.strip()

	def validate_email(self, value):
		normalized = value.strip().lower()
		if User.objects.filter(email__iexact=normalized).exists():
			raise serializers.ValidationError("Email already exists.")
		return normalized


class UserUpdateSerializer(serializers.Serializer):
	username = serializers.CharField(min_length=3, max_length=50, trim_whitespace=True, required=False)
	email = serializers.EmailField(max_length=254, required=False)
	password = serializers.CharField(min_length=6, max_length=72, trim_whitespace=False, required=False)

	def validate(self, attrs):
		user = self.context["user"]
		username = attrs.get("username")
		email = attrs.get("email")

		if username:
			username = username.strip()
			exists = User.objects.filter(username__iexact=username).exclude(pk=user.pk).exists()
			if exists:
				raise serializers.ValidationError({"message": "Username already exists."})
			attrs["username"] = username

		if email:
			email = email.strip().lower()
			exists = User.objects.filter(email__iexact=email).exclude(pk=user.pk).exists()
			if exists:
				raise serializers.ValidationError({"message": "Email already exists."})
			attrs["email"] = email

		return attrs


class UserResponseSerializer(serializers.ModelSerializer):
	createdAt = serializers.DateTimeField(source="date_joined", read_only=True)
	updatedAt = serializers.DateTimeField(source="last_login", read_only=True, allow_null=True)

	class Meta:
		model = User
		fields = ["id", "username", "email", "createdAt", "updatedAt"]


__all__ = ["UserCreateSerializer", "UserResponseSerializer", "UserUpdateSerializer"]
