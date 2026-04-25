from datetime import timedelta

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer


class LoginView(APIView):
	parser_classes = [JSONParser]

	def post(self, request):
		serializer = LoginSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		identifier = serializer.validated_data["identifier"]
		password = serializer.validated_data["password"]
		if "@" in identifier:
			matched_user = User.objects.filter(email__iexact=identifier).first()
			username = matched_user.username if matched_user else ""
			user = authenticate(username=username, password=password)
		else:
			user = authenticate(username=identifier, password=password)

		if user is None or not user.is_active:
			return Response(status=status.HTTP_401_UNAUTHORIZED)

		now = timezone.now()
		payload = {
			"sub": user.username,
			"uid": user.id,
			"iat": int(now.timestamp()),
			"exp": int((now + timedelta(milliseconds=settings.ASKNEHRU_JWT_EXPIRATION_MS)).timestamp()),
		}
		token = jwt.encode(payload, settings.ASKNEHRU_JWT_SECRET, algorithm="HS256")
		return Response(
			{
				"token": token,
				"tokenType": "Bearer",
				"user": {
					"id": user.id,
					"username": user.username,
					"email": user.email,
					"first_name": user.first_name,
					"last_name": user.last_name,
				},
			}
		)


__all__ = ["LoginView"]
