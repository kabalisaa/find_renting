from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import status, viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import jwt
from datetime import datetime, timedelta

from .serializers import UserSerializer
from renting.serializers import UserLocationSerializer
from renting.models import UserLocation

User = get_user_model()


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data['email']
            if User.objects.filter(email=user_email).exists():
                return Response({"message": "This email is already registered."}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()
            user.is_active = False
            user.save()

            # Send email with activation link
            activation_link = reverse('user-activate', kwargs={
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            activation_url = request.build_absolute_uri(activation_link)
            message = EmailMessage(
                subject='Activate your account',
                body=f'Please click on this link to activate your account: {activation_url}',
                to=[user.email],
            )
            message.send()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserActivateView(APIView):
    """API view to activate a user's account"""
    def get(self, request, uidb64, token):
        """Verify the activation token and activate the user's account"""
        try:
            uid = str(urlsafe_base64_decode(uidb64), encoding='utf-8')
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Your account has been activated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'Email not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Send email with reset_password link
        reset_password_link = reverse('password-reset-confirm', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        reset_password_url = request.build_absolute_uri(reset_password_link)
        message = EmailMessage(
            subject='Password Rest',
            body=f'Please click on this link to reset your account password: {reset_password_url}',
            to=[user.email],
        )
        message.send()
        return Response({'message': 'Password reset email sent successfully.'}, status=status.HTTP_200_OK)


class UserPasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.data)
            if form.is_valid():
                form.save()
                return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
            else:
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Password reset link is invalid."}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if email is None or password is None:
            return Response({'error': 'Please provide both email and password.'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(email=email, password=password)
        if not user:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            return Response({'error': 'User account is not active.'}, status=status.HTTP_401_UNAUTHORIZED)
        login(request, user)
        serializer = UserSerializer(user)

        # Create JWT token
        payload = {
            'user_id': user.pk,
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        response = Response(status=status.HTTP_200_OK)
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'token': token,
            'user': serializer.data,
        }
        return response


class UserViewSet(mixins.ListModelMixin, 
                  mixins.UpdateModelMixin, 
                  mixins.DestroyModelMixin, 
                  viewsets.GenericViewSet):
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        token = self.request.COOKIES.get('jwt')
        if not token:
            return Response({'error': 'Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Decode JWT token
            token = self.request.COOKIES.get('jwt')
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Unauthorized.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Get user_id from the JWT token
        user_id = decoded_token['user_id']

        # Get user object from the user_id
        user = self.queryset.filter(pk=user_id).first()

        if not user:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        if not user.is_active:
            return Response({'error': 'User account is not active.'}, status=status.HTTP_401_UNAUTHORIZED)
        return user

    def list(self, request):
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = self.get_object()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserLogoutView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        # Logout the user by removing the session data
        logout(request)
        response = Response({"success": "User logged out successfully."}, status=status.HTTP_200_OK)
        response.delete_cookie('jwt')
        return response


class UserLocationViewSet(mixins.ListModelMixin, 
                          mixins.RetrieveModelMixin, 
                          viewsets.GenericViewSet):
    serializer_class = UserLocationSerializer
    # queryset = UserLocation.objects.all()

    def get_queryset(self):
        queryset = UserLocation.objects.all()
        user_pk = self.kwargs.get('user_pk')
        location_pk = self.kwargs.get('location_pk')

        if user_pk and location_pk:
            queryset = queryset.filter(user__pk=user_pk, 
                                       pk=location_pk)
        return queryset