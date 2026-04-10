from rest_framework import serializers


class UploadResponseSerializer(serializers.Serializer):
	url = serializers.CharField()
	filename = serializers.CharField()


__all__ = ["UploadResponseSerializer"]
