import os, json
from environs import Env
from users.models import User
from django.utils import timezone
from firebase_admin import auth, credentials, initialize_app
from rest_framework import authentication
from .exceptions import FirebaseError, InvalidAuthToken, NoAuthToken


env = Env()
env.read_env()

cred = credentials.Certificate(json.loads(os.environ.get("FIREBASE_CREDENTIALS")))
default_app = initialize_app(cred)


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        # last_name = request.data.get("familyName", None)
        # first_name = request.data.get("givenName", None)
        # avatar = request.data.get("photo", None)
        # if not auth_header:
        #     raise NoAuthToken("No auth token provided")
        if auth_header is None:
            return None
        id_token = auth_header.split(" ").pop()
        # print(id_token)
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            # raise InvalidAuthToken("Invalid auth token")
            return None

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
            email = decoded_token.get("email")
            # print(decoded_token)
            # print(uid)
        except Exception:
            # raise FirebaseError()
            return None

        user, created = User.objects.get_or_create(
            username=uid,
            email=email,
            # first_name=first_name,
            # last_name=last_name,
            # avatar=avatar,
        )
        user.last_activity = timezone.localtime()

        return (user, None)