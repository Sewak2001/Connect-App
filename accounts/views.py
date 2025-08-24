from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from .models import CustomUser

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": "User registered successfully",
                "user_details": serializer.data
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email_or_phone = request.data.get("email_or_phone")
        password = request.data.get("password")

        try:
            user = CustomUser.objects.get(email=email_or_phone)
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(phone_number=email_or_phone)
            except CustomUser.DoesNotExist:
                return Response({"error": "Invalid credentials"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        user = authenticate(username=user.username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            data = {
                "message": "login successfully.",
                "access_token": str(refresh.access_token),
                'refresh_token': str(refresh),

            }
            return Response(data=data, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"},
            status=status.HTTP_400_BAD_REQUEST
        )
