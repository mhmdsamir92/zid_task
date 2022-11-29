from shipapp.models import Shipment
from Serializers.ShipmentSerializer import ShipmentSerializer
from Services.CourierServices.Courier import Courier

class ShipmentService:
    
    def create_update_shipment(self, data: dict, shipment_model: Shipment = None) -> dict:
        '''
            A function that's used to create shipment or update existing shipment
        '''
        if shipment_model:
            shipment = ShipmentSerializer(shipment_model, data=data, partial=True)
        else:
            shipment = ShipmentSerializer(data=data)
        if not shipment.is_valid():
            return {
                'status': False,
                'errors': shipment.errors
            }
        shipment.save()
        return {'status': True, 'shipment': shipment.data}


    def get_shipment_by_id(self, id: int) -> Shipment:
        return Shipment.objects.get(id=id)
    
    def get_shipment_by_tracking_id(self, tracking_id) -> Shipment:
        return Shipment.objects.get(tracking_id=tracking_id)
    
    def get_shipments_by_filters(self, filters) -> dict:
        shipments = Shipment.objects.filter(**filters)
        shipments = ShipmentSerializer(shipments, many=True)
        return shipments.data
    
    def validate_shipment_status(self, shipment: Shipment, courier: Courier, status: str) -> bool:
        if status in Shipment.SYSTEM_STATUS:
            return True
        return courier.is_status_existed(status)

