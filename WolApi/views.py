from django.shortcuts import render
from django.db import connection

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status

from .serializers import *

# Create your views here.


class NormalUserAPIView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM NormalUser')
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            result = [
                dict(zip(columns, row))
                for row in rows
            ]
        return Response(result)

    def post(self, request):
        serializer = NormalUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

