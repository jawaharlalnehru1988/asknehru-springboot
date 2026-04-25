from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
	usernameOrEmail = serializers.CharField(trim_whitespace=True, required=False, allow_blank=True)
	username = serializers.CharField(trim_whitespace=True, required=False, allow_blank=True)
	email = serializers.EmailField(required=False, allow_blank=True)
	password = serializers.CharField(trim_whitespace=False)

	def validate(self, attrs):
		identifier = (
			attrs.get("usernameOrEmail")
			or attrs.get("username")
			or attrs.get("email")
			or ""
		).strip()
		if not identifier:
			raise serializers.ValidationError({"usernameOrEmail": "This field is required."})

		attrs["identifier"] = identifier
		return attrs


__all__ = ["LoginSerializer"]
