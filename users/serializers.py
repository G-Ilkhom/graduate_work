import logging
import secrets

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""

    class Meta:
        model = User
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""

    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["first_name", "email", "password", "password2", "token"]

    def create(self, validated_data):
        password = validated_data["password"]
        password2 = validated_data.pop("password2")
        first_name = validated_data.pop("first_name")

        if password != password2:
            raise serializers.ValidationError("Пароли не совпадают")

        user = User(
            email=validated_data["email"], first_name=first_name, is_active=False
        )

        user.set_password(password)
        token = secrets.token_urlsafe(16)
        user.token = token
        user.save()
        request = self.context.get("request")
        host = request.META.get("HTTP_HOST") if request else "error"
        url = f"http://{host}/users/email_confirm/{token}/"

        try:
            send_mail(
                subject="Подтверждение почты",
                message=f"Ссылка для подтверждения почты: {url}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            logging.info(f"Письмо отправлено на почту {user.email}")
        except Exception as e:
            logging.error(f"Ошибка отправки электронной почты {user.email}: {e}")

        return user


class UserPasswordResetSerializer(serializers.Serializer):
    """Сериализатор для сброса пароля"""

    email = serializers.EmailField()

    def save(self):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        host = "http://127.0.0.1:8000"
        url = f"http://{host}/users/reset_password/{uid}/{token}/"
        send_mail(
            subject="Сброс пароля",
            message=f"Ссылка для сброса вашего пароля: {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )


class UserPasswordResetConfirmSerializer(serializers.Serializer):
    """Сериализатор для подтверждения сброса пароля"""

    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        uid = attrs["uid"]
        token = attrs["token"]
        new_password = attrs["new_password"]

        print(f"uid: {uid}")
        print(f"token: {token}")

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
            if not default_token_generator.check_token(user, token):
                raise serializers.ValidationError("Неверный токен")
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Неверный uid или токен")

        attrs["user"] = user
        attrs["new_password"] = new_password
        return attrs

    def save(self):
        user = self.validated_data["user"]
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save()


class LoginSerializer(serializers.Serializer):
    """Сериализатор для входа пользователя"""

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )
            if not user:
                raise serializers.ValidationError("Неверные учетные данные")
        else:
            raise serializers.ValidationError(
                "Необходимо ввести адрес электронной почты и пароль"
            )

        data["user"] = user
        return data
