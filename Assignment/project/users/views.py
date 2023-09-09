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



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('name')
        password = request.data.get('password')

        # Check if both username and password are provided
        if not (username and password):
            raise AuthenticationFailed('Both username and password are required.')

        user = RegisterUser.objects.filter(name=username).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        # Generate JWT token
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        # Set the token in response
        response = Response({
            'status': 'success',
            'message': 'Access token generated successfully.',
            'data': {
                'access_token': token,
                'expires_in': 3600
            }
        })

        return response


class UserView(APIView):
    permission_classes = [AllowAny]
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









