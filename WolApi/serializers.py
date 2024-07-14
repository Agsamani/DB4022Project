from rest_framework import serializers
from django.db import connection
from django.contrib.auth.models import User

from . import utils
from datetime import datetime
from .elastic_utils import index_advertisement

# TODO: How to handle errors raised in sql?
class NormalUserSerializer(serializers.Serializer):
    isactive = serializers.BooleanField(default=True)
    firstname = serializers.CharField(max_length=255)
    lastname = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False, max_length=11, min_length=11)
    cityid = serializers.IntegerField()

    def validate(self, attrs):
        # TODO : Maybe check city?
        if attrs.get("email") is None and attrs.get("phone") is None:
            raise serializers.ValidationError("Email and Phone cant be both null")
        if "phone" in attrs and len(attrs["phone"]) != 11:
            raise serializers.ValidationError("Invalid phone number")
        return attrs

    def create(self, validated_data):

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM NormalUser WHERE email = %s OR phone = %s",
                [validated_data.get('email'), validated_data.get('phone')]
            )
            if cursor.fetchone() is not None:
                raise serializers.ValidationError("Email or Phone already exists")
            cursor.execute(
                "INSERT INTO Publisher (isactive, regdate) VALUES (%s, %s) RETURNING pubid",
                [validated_data.get("isactive"),
                 datetime.now()]
            )
            pubid = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO NormalUser (PubID, FirstName, LastName, Email, Phone, CityID) "
                "values (%s, %s, %s, %s, %s, %s);",
                [pubid,
                 validated_data.get('firstname'),
                 validated_data.get('lastname'),
                 validated_data.get('email'),
                 validated_data.get('phone'),
                 validated_data.get('cityid')]
            )
        User.objects.create(username=pubid,
                            email=validated_data.get('email') if 'email' in validated_data else validated_data.get('phone'),
                            password="12345678")
        return validated_data


class AdminSerializer(serializers.Serializer):
    adminid = serializers.IntegerField(required=False)
    firstname = serializers.CharField(max_length=255)
    lastname = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False, max_length=11, min_length=11)

    def validate(self, attrs):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM NormalUser WHERE email = %s OR phone = %s",
                [attrs.get('email'), attrs.get('phone')]
            )
            if cursor.fetchone() is not None:
                raise serializers.ValidationError("Email or Phone already exists")
        if attrs.get("email") is None and attrs.get("phone") is None:
            raise serializers.ValidationError("Email and Phone cant be both null")
        if "phone" in attrs and len(attrs["phone"]) != 11:
            raise serializers.ValidationError("Invalid phone number")
        return attrs

    def create(self, validated_data):
        with connection.cursor() as cursor:

            cursor.execute(
                "INSERT INTO Administrator (FirstName, LastName, Email, Phone)"
                "values (%s, %s, %s, %s) RETURNING AdminID;",
                [validated_data.get('firstname'),
                 validated_data.get('lastname'),
                 validated_data.get('email'),
                 validated_data.get('phone')]
            )
            adminid = cursor.fetchone()[0]

        User._meta.get_field('username')._unique = False
        User.objects.create(username=adminid,
                            email=validated_data.get('email') if 'email' in validated_data else validated_data.get('phone'),
                            password="admin12345678",
                            is_staff=True)

        return validated_data


class AdvertisementSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(required=False, max_digits=14, decimal_places=4)
    cityid = serializers.IntegerField()  # TODO : Maybe check city?
    addesc = serializers.CharField(max_length=511)
    catid = serializers.IntegerField() # TODO : check category

    # Category specific fields
    brand = serializers.CharField(max_length=255, required=False)
    material = serializers.CharField(max_length=255, required=False)
    productionyear = serializers.IntegerField(required=False)
    area = serializers.IntegerField(required=False)
    constructiondate = serializers.DateField(required=False)
    model = serializers.CharField(max_length=255, required=False)


    def create(self, validated_data):
        with connection.cursor() as cursor:
            temp_time = datetime.now()
            cursor.execute(
                "INSERT INTO Advertisement (PubID, Title, Price, CreationDate, CityID, UpdateDate, AdDesc, CatID)"
                "values (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING AdvertisementID;",
                [self.context['pubId'],
                 validated_data.get('title'),
                 validated_data.get('price'),
                 temp_time,
                 validated_data.get('cityid'),
                 temp_time,
                 validated_data.get('addesc'),
                 validated_data.get('catid')]
            )
            temp_time = datetime.now()
            adId = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO AdStatus (AdvertisementID, AdStateID, UpdatedAt) "
                "values(%s, %s, %s)",
                [adId,
                 0,
                 temp_time]
            )
            match int(validated_data.get('catid')):
                case 0:
                    cursor.execute(f"INSERT INTO Other (AdvertisementID) VALUES (%s)",
                                   adId)
                case 1:
                    cursor.execute(f"INSERT INTO HomeAppliance (AdvertisementID, Brand, Material) VALUES (%s, %s, %s)",
                                   [adId, validated_data.get('brand'), validated_data.get('material')])
                case 2:
                    cursor.execute(f"INSERT INTO Vehicle (AdvertisementID, Brand, ProductionYear) VALUES (%s, %s, %s)",
                                   [adId, validated_data.get('brand'), validated_data.get('productionyear')])
                case 3:
                    cursor.execute(f"INSERT INTO RealEstate (AdvertisementID, Area, ConstructionDate) VALUES (%s, %s, %s)",
                                   [adId, validated_data.get('area'), validated_data.get('constructiondate')])
                case 4:
                    cursor.execute(f"INSERT INTO DigitalProduct (AdvertisementID, Brand, Model) VALUES (%s, %s, %s)",
                                   [adId, validated_data.get('brand'), validated_data.get('model')])

            for img in self.context.get('images'):
                cursor.execute(
                    "INSERT INTO Images (AdvertisementID, Url) VALUES (%s, %s) RETURNING ImageID",
                    [adId, ""]
                )
                imageId = cursor.fetchone()[0]
                url = utils.save_request_image(img, imageId)
                cursor.execute(
                    "UPDATE Images SET Url = %s WHERE ImageID = %s",
                    [str(url), adId]
                )
            ad_data = {
                'AdvertisementID': adId,
                'Title': validated_data.get('title'),
                'Price': validated_data.get('price'),
                'CreationDate': temp_time,
                'IsActive': True
            }
            index_advertisement(ad_data=ad_data)

        return validated_data


class AdStatusSerializer(serializers.Serializer):
    adState = serializers.CharField(max_length=255)
    adminComment = serializers.CharField(required=False, max_length=255)

    def validate(self, attrs):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT AdStateName FROM StatusState"
            )

            if attrs.get("adState").upper() not in [x for (x,) in cursor.fetchall()]:
                raise serializers.ValidationError(f"Unknown ad state {attrs.get('adState')}")

        return attrs

    def create(self, validated_data):
        temp_time = datetime.now()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT AdStateID FROM StatusState WHERE AdStateName = %s",
                [validated_data.get('adState').upper()]
            )

            adStateId = cursor.fetchone()[0]
            adminId = self.context['adminId']
            adId = self.context['adId']

            cursor.execute(
                "UPDATE AdStatus SET AdStateID = %s, AdminComment = %s, UpdatedAt = %s WHERE AdvertisementID = %s",
                [adStateId, self.validated_data['adminComment'], temp_time, adId]
            )

            cursor.execute(
                "INSERT INTO Modified (AdminID, AdvertisementID, ModDate, ToStateID) "
                "VALUES (%s, %s, %s, %s)",
                [adminId, adId, temp_time, adStateId]
            )

        return validated_data

class BusinessSerializer(serializers.Serializer):
    bname = serializers.CharField(max_length=255)
    catid = serializers.IntegerField(default=0)
    registerationnum = serializers.IntegerField()
    cityid = serializers.IntegerField()

    def create(self, validated_data):
        with connection.cursor() as cursor:
            # TODO : Check Cat and City
            isactive = validated_data["isactive"] if "isactive" in validated_data else True
            cursor.execute(
                "INSERT INTO Publisher (isactive, regdate) VALUES (%s, %s) RETURNING pubid",
                [isactive,
                 datetime.now()]
            )
            pubid = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO Business (PubID, UserID, BName, CatID, RegistrationNum, CityID) "
                "values (%s, %s, %s, %s, %s, %s);",
                [pubid,
                 self.context.get('userId'),
                 validated_data.get('bname'),
                 validated_data.get('catid'),
                 validated_data.get('registerationnum'),
                 validated_data.get('cityid')]
            )
        return validated_data


class ReportSerializer(serializers.Serializer):
    catid = serializers.IntegerField(default=0)
    rdesc = serializers.CharField(required=False, max_length=511)

    def create(self, validated_data):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT UserID FROM Report WHERE UserID = %s",
                [self.context['userId']]
            )
            if cursor.fetchone():
                raise serializers.ValidationError("User already reported this add")

            cursor.execute("INSERT INTO Report (AdvertisementID, UserID, CatID, RDesc) "
                           "VALUES (%s, %s, %s, %s)",
                           [self.context['adId'],
                            self.context['userId'],
                            self.validated_data.get('catid'),
                            self.validated_data.get('rdesc')])

        return validated_data

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'email']