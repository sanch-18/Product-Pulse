from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import random
from .utils import Util
from datetime import timedelta
from django.utils import timezone
from .models import User, UserDetails

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        try:
            email = request.data.get('email')
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                is_verified = user.is_verified
                if (not is_verified) and (timezone.now() > user.created_at + timedelta(minutes=10)):
                    user.delete()
                    x = UserDetails.objects.get(user=user)
                    x.delete()
                else :
                    return Response("User email account already exists can't create one!")
        except:
            return Response("Please give a valid input!", status=status.HTTP_400_BAD_REQUEST)
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            member = UserDetails(name=request.data.get('name'), email=request.data.get('email'), phone=request.data.get('phone'), user=user)
            member.save()
            try:
                otp = str(random.randint(100000, 999999))
                user.otp = otp

                user.save()
                body = f'Your OTP code is {otp}'
                data = {
                    'subject': 'Your OTP code',
                    'body': body,
                    'to_email': user.email
                }
                Util.send_email(data)
                return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        try:
            user = User.objects.get(email=email)
            if user.otp == otp and timezone.now() < user.created_at + timedelta(minutes=10):
                user.otp = None  # Clear OTP after successful verification
                user.is_verified = True
                user.save()
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'OTP Verified Successfully, Registration successfull'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            if User.objects.filter(email=email).exists():
                USER = User.objects.get(email = email)
                if not USER.is_verified:
                    return Response({'errors' : 'User not Verified'})
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'msg' : 'Logout Successful!'},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]

  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)

class DeleteUserAccount(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        try:
            user.delete()
            msg = f"User '{user.email}' has been deleted."
            res = {
                'msg' : msg,
            }
        except user.DoesNotExist:
            res = {
                'errors' : "User not found",
            }
        return Response(res)