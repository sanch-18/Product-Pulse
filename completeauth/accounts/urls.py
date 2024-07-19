from django.urls import path, include
from .views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView, SendPasswordResetEmailView, UserPasswordResetView, DeleteUserAccount, VerifyOTPView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="Register"),
    path('verify-OTP/', VerifyOTPView.as_view(), name="VerifyOTP"),
    path('login/', UserLoginView.as_view(), name="Login"),
    path('logout/', LogoutView.as_view(), name="Logout"),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name="Profile"),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('Delete-User/', DeleteUserAccount.as_view(), name="Delete-User"),
]
