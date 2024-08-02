from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (UserLoginView, UserPasswordResetConfirmView,
                         UserPasswordResetView, UserRegisterView,
                         UserRetrieveView, email_confirm)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("email_confirm/<str:token>/", email_confirm, name="email_confirm"),
    path("<int:pk>/", UserRetrieveView.as_view(), name="user_detail"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("reset_password/", UserPasswordResetView.as_view(), name="reset_password"),
    path(
        "reset_password_confirm/",
        UserPasswordResetConfirmView.as_view(),
        name="reset_password_confirm",
    ),
]
