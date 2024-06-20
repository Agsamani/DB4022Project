from django.shortcuts import render
from django.db import connection

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from . import utils

# Create your views here.

@api_view(['POST'])
def get_otp(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT pubid FROM NormalUser WHERE email = %s OR phone = %s',
                       [request.data.get('email'),
                        request.data.get('phone')])
        result = cursor.fetchone()

    if result is None:
        return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)
    otp = utils.generate_otp(result[0])
    return Response(otp)


@api_view(['POST'])
def login(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT pubid FROM NormalUser WHERE email = %s OR phone = %s',
                       [request.data.get('email'),
                        request.data.get('phone')])
        result = cursor.fetchone()

    if result is None:
        return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)

    if not utils.validate_otp(result[0], request.data.get('otp')):
        return Response("Invalid password", status=status.HTTP_401_UNAUTHORIZED)

    # TODO: should change?
    custom_user = User.objects.get(id=result[0])
    user_serializer = UserSerializer(custom_user)
    token, created = Token.objects.get_or_create(user=custom_user)
    resp = Response({"token": token.key, "user": user_serializer.data})
    resp.set_cookie(key='token', value=token.key, httponly=True)
    return resp


@api_view(['POST'])
def admin_get_otp(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT AdminID FROM Administrator WHERE email = %s OR phone = %s',
                       [request.data.get('email'),
                        request.data.get('phone')])
        result = cursor.fetchone()

    if result is None:
        return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)
    otp = utils.generate_otp(result[0])
    return Response(otp)


@api_view(['POST'])
def admin_login(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT AdminID FROM Administrator WHERE email = %s OR phone = %s',
                       [request.data.get('email'),
                        request.data.get('phone')])
        result = cursor.fetchone()

    if result is None:
        return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)

    if not utils.validate_otp(result[0], request.data.get('otp')):
        return Response("Invalid password", status=status.HTTP_401_UNAUTHORIZED)

    # TODO: should change?
    custom_user = User.objects.get(id=result[0])
    user_serializer = UserSerializer(custom_user)
    token, created = Token.objects.get_or_create(user=custom_user)
    resp = Response({"token": token.key, "admin": user_serializer.data})
    resp.set_cookie(key='token', value=token.key, httponly=True)
    return resp

@api_view(['GET']) # Only for test, Will get removed
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    print(request.user)
    return Response("Passed")


class UserAPIView(APIView):
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


class AdminAPIView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM Administrator')
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            result = [
                dict(zip(columns, row))
                for row in rows
            ]
        return Response(result)

    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdvertisementAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM Advertisement')
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            result = [
                dict(zip(columns, row))
                for row in rows
            ]
        return Response(result)

    def post(self, request):
        serializer = AdvertisementSerializer(data=request.data) # TODO : .dict or not .dict? Ajax or not Ajax?
        serializer.set_pubid(request.user.username)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)