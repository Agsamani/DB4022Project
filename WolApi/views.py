from datetime import time

from django.shortcuts import render
from django.db import connection

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

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
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
def test_token(request):
    return Response("Passed")


class UserAPIView(APIView):  # TODO : declass these
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

    def get(self, request): # TODO: Wot is this
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM Advertisement '
                           'JOIN Publisher ON Publisher.pubId = Advertisement.pubId '
                           'WHERE Advertisement.IsActive = TRUE AND Publisher.IsActive = TRUE '
                           )
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            result = [
                dict(zip(columns, row))
                for row in rows
            ]
        return Response(result)

    def post(self, request):
        serializer = AdvertisementSerializer(data=request.data, context={"pubId": request.user.username, "images": request.FILES.getlist('images')}) # TODO : .dict or not .dict? Ajax or not Ajax?
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAdminUser])
def admin_update_ad_status(request, ad_id):
    serializer = AdStatusSerializer(data=request.data, context={"adminId": 1, "adId": ad_id})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_latest_ads(request):
    lim = request.GET.get('limit', 10)
    with connection.cursor() as cursor:
        # TODO: Maybe return publisher and business name
        cursor.execute('SELECT AdvertisementID, Title, Price, CreationDate FROM Advertisement '
                       'JOIN Publisher ON Publisher.pubId = Advertisement.pubId '
                       'WHERE Advertisement.IsActive = TRUE AND Publisher.IsActive = TRUE '
                       'ORDER BY CreationDate DESC LIMIT %s',
                       [lim])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        result = [
            dict(zip(columns, row))
            for row in rows
        ]
    return Response(result)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([AllowAny])
def get_ad_detail(request, ad_id):
    with connection.cursor() as cursor:
        # TODO: Maybe return publisher and business name
        cursor.execute('SELECT * FROM Advertisement '
                       'LEFT JOIN Vehicle ON Advertisement.AdvertisementId = Vehicle.AdvertisementId '
                       'LEFT JOIN RealEstate ON Advertisement.AdvertisementId = RealEstate.AdvertisementId '
                       'LEFT JOIN HomeAppliance ON Advertisement.AdvertisementId = HomeAppliance.AdvertisementId '
                       'LEFT JOIN DigitalProduct ON Advertisement.AdvertisementId = DigitalProduct.AdvertisementId '
                       'WHERE Advertisement.AdvertisementID = %s',
                       [ad_id])
        rows = cursor.fetchall()
        if len(rows) == 0:
            return Response("Invalid object key", status=status.HTTP_404_NOT_FOUND)
        columns = [col[0] for col in cursor.description]
        result = [
            dict(zip(columns, row))
            for row in rows
        ]
        if not request.user.is_anonymous:
            userId = request.user.username
            temp_time = datetime.now()
            cursor.execute("INSERT INTO Visit (UserID, AdvertisementID, VisitTime) VALUES (%s, %s, %s)",
                           [userId, ad_id, temp_time])
    return Response(result)

@api_view(['PUT'])  # TODO: Check if works with permissions
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    serializer = NormalUserSerializer(data=request.data)
    if serializer.is_valid():
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE NormalUser SET FirstName = %s, LastName = %s, Email = %s,  Phone = %s,  CityID = %s WHERE PubID = %s",
                [serializer.validated_data.get('firstname'),
                 serializer.validated_data.get('lastname'),
                 serializer.validated_data.get('email'),
                 serializer.validated_data.get('phone'),
                 serializer.validated_data.get('cityid'),
                 request.user.username]
            )

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])  
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_ads(request):
    lim = request.GET.get('limit', 10)
    with connection.cursor() as cursor:
        # TODO: Maybe return publisher and business name
        cursor.execute('SELECT AdvertisementID, Title, Price, CreationDate FROM Advertisement WHERE PubID = %s '
                       'ORDER BY CreationDate DESC LIMIT %s',
                       [request.user.username, lim])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        result = [
            dict(zip(columns, row))
            for row in rows
        ]
    return Response(result)


@api_view(['POST'])  # TODO: Check if works with permissions
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def new_business(request):
    serializer = BusinessSerializer(data=request.data, context={"userId": request.user.username})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def report_ad(request, ad_id):
    serializer = ReportSerializer(data=request.data, context={"userId": request.user.username, "adId": ad_id})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAdminUser])
def get_ad_reports(request, ad_id):
    lim = request.GET.get('limit', 10)
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Report WHERE AdvertisementID = %s LIMIT %s',
                       [ad_id, lim])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        result = [
            dict(zip(columns, row))
            for row in rows
        ]
    return Response(result)


@api_view(['PATCH'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAdminUser])
def deactivate_ad(request, ad_id):
    with connection.cursor() as cursor:
        cursor.execute('UPDATE Advertisement SET IsActive = FALSE WHERE AdvertisementID = %s',
                       [ad_id])
    return Response(status.HTTP_200_OK)


@api_view(['PATCH'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def deactivate_user(request, pub_id):
    with connection.cursor() as cursor:
        cursor.execute('UPDATE Publisher SET IsActive = FALSE WHERE PubID = %s',
                       [pub_id])
    return Response(status.HTTP_200_OK)


@api_view(['GET'])
def search_advertisement(request):
    search_string = request.GET.get('search_string', "")
    catid = request.GET.get('catid', None)
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT advertisement.* FROM advertisement "
                        "JOIN Publisher ON Publisher.pubId = Advertisement.pubId "
                        "WHERE Advertisement.IsActive = TRUE AND Publisher.IsActive = TRUE "
                       f"AND title LIKE '%{search_string}%'" +
                       (f"AND catid = {catid}" if catid else ""),)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        result = [
            dict(zip(columns, row))
            for row in rows
        ]
    return Response(result)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def file_test(request):
    f = request.FILES.getlist('s')
    a =0
    for i in f:
        if 'png' or 'jpeg' in i.content_type: # TODO: check file size
            print(i.name)
            utils.save_request_image(i, a)
            a += 1


    return Response("hi")


@api_view(['GET'])
def hello_react(request):
    return Response("~Hello, React!")