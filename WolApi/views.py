from django.shortcuts import render
from django.db import connection
from rest_framework import status

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import PublisherSerializer

# Create your views here.
@api_view(['GET'])
def sandbox(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Publisher')
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        result = [
            dict(zip(columns, row))
            for row in rows
        ]
    serializer = PublisherSerializer(result, many=True)
    return Response(result)

@api_view(['POST'])
def sandbox_add(request):
    serializer = PublisherSerializer(data=request.data)
    if serializer.is_valid():
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO publisher (pubid, isactive, regdate) VALUES (%s, %s, %s)",
                [serializer.validated_data['pubid'], serializer.validated_data['isactive'],
                 serializer.validated_data['regdate']]
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
