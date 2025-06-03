from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
 

def custom200(message, data=None):
    return Response({
        "status": "Success",
        "status_code": 200,
        "message": message,
        "data": data if data is not None else {}
    }, status=status.HTTP_200_OK)

def custom201(message, data=None):
    return Response({
        "status": "Created",
        "status_code": 201,
        "message": message,
        "data": data if data is not None else {}
    }, status=status.HTTP_201_CREATED)

def custom400(message, errors=None):
    return Response({
        "status": "Bad Request",
        "status_code": 400,
        "message": message,
        "errors": errors if errors is not None else {}
    }, status=status.HTTP_400_BAD_REQUEST)

def custom404(request, message):
    return Response({
        "status": "Failed 'Not Found'",
        "status_code": 404,
        "message": message
    }, status=status.HTTP_404_NOT_FOUND)