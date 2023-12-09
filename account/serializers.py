from djoser.serializers import UserCreateSerializer
from account.models import User

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'profile_image')  # Add 'profile_image'
