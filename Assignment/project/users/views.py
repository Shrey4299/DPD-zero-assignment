from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import RegisterUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime



class CustomUserCreate(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):

        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserById(APIView):
    def get(self, request, user_id):
        try:
            user = RegisterUser.objects.get(id=user_id)
            serializer = CustomUserSerializer(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except RegisterUser.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, user_id):
        try:
            user = RegisterUser.objects.get(phone_number=request.data.get("phone_number"))
            user.name = request.data.get("name")
            user.save()
            return Response({"message": "name field updated successfully."}, status=status.HTTP_200_OK)
        except RegisterUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = RegisterUser.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        #
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        #
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=False)
        response.data = {
            'jwt': token,
            'id': user.id,
        }
        return response


class UserView(APIView):
    def get(self, request, format='json'):
        token = request.data.get('jwt')  # Get the token from the request body

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256')  # Pass algorithm as a string, not a list
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = RegisterUser.objects.filter(id=payload['id']).first()
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)









