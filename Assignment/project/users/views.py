from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import RegisterUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        age = request.data.get('age')
        if age is not None and (not isinstance(age, int) or age <= 0):
            response_data = {
                "status": "error",
                "code": "INVALID_AGE",
                "message": "Invalid age value. Age must be a positive integer."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        password = request.data.get('password')
        if not (any(c.isupper() for c in password) and
                any(c.islower() for c in password) and
                any(c.isdigit() for c in password) and
                any(c in "!@#$%^&*()-_+=<>,.?/:;{}[]|\\~" for c in password)):
            response_data = {
                "status": "error",
                "code": "INVALID_PASSWORD",
                "message": "Invalid password. Password must be at least 8 characters long and contain a mix of uppercase and lowercase letters, numbers, and special characters."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        username = request.data.get('username')
        email = request.data.get('email')

        if RegisterUser.objects.filter(username=username).exists():
            response_data = {
                "status": "error",
                "code": "USERNAME_EXISTS",
                "message": "The provided username is already taken. Please choose a different username."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if RegisterUser.objects.filter(email=email).exists():
            response_data = {
                "status": "error",
                "code": "EMAIL_EXISTS",
                "message": "The provided email is already registered. Please use a different email address."
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                user_data = {
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.full_name,
                    "age": user.age,
                    "gender": user.gender
                }

                response_data = {
                    "status": "success",
                    "message": "User successfully registered!",
                    "data": user_data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)

        response_data = {
            "status": "error",
            "code": "INVALID_REQUEST",
            "message": "Invalid request. Please provide all required fields: username, email, password, full_name."
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
