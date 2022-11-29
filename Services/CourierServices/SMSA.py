import abc
from .Courier import Courier
from Serializers.ShipmentSerializer import ShipmentSerializer
from shipapp.models import Shipment
import logging
import uuid

logger = logging.getLogger(__name__)

class SMSA(Courier):

    SMSA_STATUSES_MAPPER = {
        "PENDING": Shipment.PENDING,
        "PLANNED": Shipment.PENDING,
        "ON_THE_WAY": Shipment.TRANSIT,
        "CLIENT_RECEIVED": Shipment.DELIVERED,
        "EXPIRED": Shipment.FAILED,
    }
    
    def create_waybill(self, data: dict) -> str:
        logger.info("Calling SMSA to get waybill")
        return str(uuid.uuid1())

    def get_waybill_label(self, tracking_id: int) -> list:
        return [
            f"SMSA report for {tracking_id}"
        ]

    def retrieve_waybill_status(self) -> list:
        return self.SMSA_STATUSES_MAPPER