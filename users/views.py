from django.middleware.csrf import get_token
from django.shortcuts import redirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import (LoginSerializer,
                               UserPasswordResetConfirmSerializer,
                               UserPasswordResetSerializer,
                               UserRegisterSerializer, UserSerializer)


class UserRegisterView(APIView):
    """Регистрация пользователя"""

    def post(self, request):
        serializer = UserRegisterSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def email_confirm(request, token):
    """Подтверждение почты"""

    try:
        user = User.objects.get(token=token)
        user.is_active = True
        user.token = ""
        user.save()
        return redirect("/")
    except User.DoesNotExist:
        return redirect("http://127.0.0.1:8000/users/register")


class UserLoginView(APIView):
    """Вход в учетную запись"""

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        response = Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "csrftoken": get_token(request),
            },
            status=status.HTTP_200_OK,
        )
        return response


class UserRetrieveView(generics.RetrieveAPIView):
    """Вывод одного пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserPasswordResetView(APIView):
    """Сброс пароля"""

    def post(self, request):
        serializer = UserPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"На почту отправлена инструкция по сбросу пароля."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetConfirmView(APIView):
    """Подтверждение сброса пароля"""

    def post(self, request):
        serializer = UserPasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Пароль был успешно сменен."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
