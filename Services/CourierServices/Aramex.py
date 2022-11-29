import abc
from .Courier import Courier
from .CancellableCourier import CancellableCourier
from Serializers.ShipmentSerializer import ShipmentSerializer
from shipapp.models import Shipment
import uuid
import logging

logger = logging.getLogger(__name__)

class Aramex(Courier, CancellableCourier):

    ARAMEX_STATUSES_MAPPER = {
        "PENDING": Shipment.PENDING,
        "SCHEDULUED": Shipment.PENDING,
        "TRANSIT": Shipment.TRANSIT,
        "RECEIVED": Shipment.DELIVERED,
        "EXPIRED": Shipment.FAILED,
    }
    
    def create_waybill(self, data: dict) -> str:
        logger.info("Calling Aramex to get waybill")
        return str(uuid.uuid1())

    def get_waybill_label(self, tracking_id: int) -> list:
        return [
            f"Aramex report for {tracking_id}"
        ]

    def retrieve_waybill_status(self) -> list:
        return self.ARAMEX_STATUSES_MAPPER
    
    def cancel(self, shipment: Shipment) -> bool:
        logger.info('Sending request to aramex to cancel this request')
        return True