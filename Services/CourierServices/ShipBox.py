import abc
from .Courier import Courier
from Serializers.ShipmentSerializer import ShipmentSerializer
from shipapp.models import Shipment
import logging
import uuid

logger = logging.getLogger(__name__)

class ShipBox(Courier):

    SHIPBOX_STATUSES_MAPPER = {
        "ADDED": Shipment.PENDING,
        "CHECKING": Shipment.PENDING,
        "DEPARTED": Shipment.TRANSIT,
        "DELIVERED": Shipment.DELIVERED,
        "EXPIRED": Shipment.FAILED,
    }
    
    def create_waybill(self, data: dict) -> str:
        logger.info("Calling ShipBox to get waybill")
        return str(uuid.uuid1())

    def get_waybill_label(self, tracking_id: int) -> list:
        return [
            f"ShipBox report for {tracking_id}"
        ]

    def retrieve_waybill_status(self) -> list:
        return self.SHIPBOX_STATUSES_MAPPER