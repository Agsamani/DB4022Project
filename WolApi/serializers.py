from rest_framework import serializers
from django.db import connection
from django.contrib.auth.models import User


from datetime import datetime


class NormalUserSerializer(serializers.Serializer):
    pubid = serializers.IntegerField(required=False)
    isactive = serializers.BooleanField(required=False)
    firstname = serializers.CharField(max_length=255)
    lastname = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False, max_length=11, min_length=11)
    cityid = serializers.IntegerField()

    def validate(self, attrs):
        # TODO : Maybe check city?
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
            isactive = validated_data["isactive"] if "isactive" in validated_data else True
            cursor.execute(
                "INSERT INTO Publisher (isactive, regdate) VALUES (%s, %s) RETURNING pubid",
                [isactive,
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
        User.objects.create(id=pubid,
                                   username=validated_data.get('firstname') + "_" + validated_data.get('lastname'),
                                   email=validated_data.get('email'),
                                   password="12345678")
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'email']