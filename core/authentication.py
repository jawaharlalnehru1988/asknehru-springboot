from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
import jwt


class AskNehruJWTAuthentication(BaseAuthentication):
    keyword = b"Bearer"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower():
            return None

        if len(auth) != 2:
            raise AuthenticationFailed("Invalid Authorization header format.")

        token = auth[1]
        try:
            payload = jwt.decode(token, settings.ASKNEHRU_JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        username = payload.get("sub")
        if not username:
            raise AuthenticationFailed("Invalid token payload.")

        user = User.objects.filter(username=username, is_active=True).first()
        if user is None:
            raise AuthenticationFailed("User not found.")

        return (user, None)

    def authenticate_header(self, request):
        return "Bearer"
