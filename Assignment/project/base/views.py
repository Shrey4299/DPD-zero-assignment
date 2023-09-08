from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .model import KeyValue
from .serializer import KeyValueSerializer


class KeyValueAPIView(APIView):
    def post(self, request, format=None):
        key = request.data.get('key')
        value = request.data.get('value')

        if not key:
            return Response({'status': 'error', 'message': 'Invalid or missing key.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not value:
            return Response({'status': 'error', 'message': 'Invalid or missing value.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if KeyValue.objects.filter(key=key).exists():
            return Response({'status': 'error', 'message': 'Key already exists. Use the update API.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = KeyValueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Data stored successfully.'},
                            status=status.HTTP_201_CREATED)

        return Response({'status': 'error', 'message': 'Invalid data provided.'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, key, format=None):
        try:
            key_value = KeyValue.objects.get(key=key)
            serializer = KeyValueSerializer(key_value)
            return Response({
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except KeyValue.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Key not found.'
            }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, key, format=None):
        try:
            key_value = KeyValue.objects.get(key=key)
            value = request.data.get('value')

            if value is not None:
                serializer = KeyValueSerializer(key_value, data={'value': value}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'status': 'success',
                        'message': 'Data updated successfully.'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'status': 'error',
                        'message': 'Invalid data provided.',
                        'errors': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'status': 'error',
                    'message': 'Invalid or missing value.'
                }, status=status.HTTP_400_BAD_REQUEST)

        except KeyValue.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Key not found.'
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, key, format=None):
        try:
            key_value = KeyValue.objects.get(key=key)
            key_value.delete()
            return Response({
                'status': 'success',
                'message': 'Data deleted successfully.'
            }, status=status.HTTP_200_OK)
        except KeyValue.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Key not found.'
            }, status=status.HTTP_404_NOT_FOUND)
