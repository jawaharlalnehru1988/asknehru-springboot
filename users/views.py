from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserCreateSerializer, UserResponseSerializer, UserUpdateSerializer


class UsersView(APIView):
	parser_classes = [JSONParser]

	def get(self, request):
		users = User.objects.order_by("id")
		return Response(UserResponseSerializer(users, many=True).data)

	def post(self, request):
		serializer = UserCreateSerializer(data=request.data)
		if not serializer.is_valid():
			message = next(iter(serializer.errors.values()))[0]
			return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

		user = User.objects.create_user(
			username=serializer.validated_data["username"],
			email=serializer.validated_data["email"],
			password=serializer.validated_data["password"],
		)
		return Response(UserResponseSerializer(user).data, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
	parser_classes = [JSONParser]

	def get_object(self, pk: int) -> User:
		user = User.objects.filter(pk=pk).first()
		if user is None:
			raise Http404
		return user

	def get(self, request, pk: int):
		return Response(UserResponseSerializer(self.get_object(pk)).data)

	def put(self, request, pk: int):
		user = self.get_object(pk)
		serializer = UserUpdateSerializer(data=request.data, context={"user": user})
		if not serializer.is_valid():
			message = serializer.errors.get("message", [None])[0]
			if message is None:
				first_error = next(iter(serializer.errors.values()))
				message = first_error[0] if isinstance(first_error, list) else str(first_error)
			return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

		data = serializer.validated_data
		if "username" in data:
			user.username = data["username"]
		if "email" in data:
			user.email = data["email"]
		if "password" in data:
			user.set_password(data["password"])
		user.save()
		return Response(UserResponseSerializer(user).data)

	def delete(self, request, pk: int):
		user = self.get_object(pk)
		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


__all__ = ["UsersView", "UserDetailView"]
