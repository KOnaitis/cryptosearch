from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, CharField

UserModel = get_user_model()


class UserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    def create(self, validated_data):
        return UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

    class Meta:
        model = UserModel
        fields = ('username', 'password',)
