from rest_framework import serializers
from shipapp.models import Shipment


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'

    