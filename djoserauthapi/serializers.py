# custom_serializers.py
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken


class InActiveUser(AuthenticationFailed):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = "User is not active, please confirm your email"
    default_code = 'user_is_inactive'


# noinspection PyAbstractClass
class CustomTokenObtainPairSerializer(TokenObtainSerializer):

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_active:
            raise InActiveUser()

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

# custom_authentication.py
def custom_user_authentication_rule(user):
    """
    Override the default user authentication rule for Simple JWT Token to return true if there is a user and let
    serializer check whether user is active or not to return an appropriate error
    :param user: user to be authenticated
    :return: True if user is not None
    """

    return True if user is not None else False



