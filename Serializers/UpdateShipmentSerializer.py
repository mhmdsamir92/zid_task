from rest_framework import serializers

class UpdateShipmentSerializerRequest(serializers.Serializer):
    id = serializers.IntegerField()
    tracking_id = serializers.CharField()


