from rest_framework import serializers

class PublisherSerializer(serializers.Serializer):
    pubid = serializers.IntegerField()
    isactive = serializers.BooleanField()
    regdate = serializers.DateTimeField()

    def create(self, validated_data):
        print(validated_data)
        return validated_data