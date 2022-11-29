from Services.CourierServices.Courier import Courier
from Services.ShipmentServices.ShipmentService import ShipmentService
from Services.CourierServices.CourierFactory import CourierFactory
from Services.CourierServices.CancellableCourier import CancellableCourier
from shipapp.models import Shipment # TODO: This depedency should be removed, controller shouldn't be aware of model layer
import io
import logging
from reportlab.pdfgen import canvas

logger = logging.getLogger(__name__)

class ShipmentController:

    def __init__(self, shipment_service: ShipmentService, courier_factory: CourierFactory) -> None:
        self.shipment_service = shipment_service
        self.courier_factory = courier_factory

    def create_shipment(self, data: dict):
        courier = self.courier_factory.create_courier(data['provider'])
        tracking_id = courier.create_waybill(data)
        data['tracking_id'] = tracking_id
        return self.shipment_service.create_update_shipment(data)

    def print_waybill_label(self, id: int) -> io.BytesIO:
        shipment = self.shipment_service.get_shipment_by_id(id)
        provider = shipment.provider
        courier = self.courier_factory.create_courier(provider)
        printable_strings = courier.get_waybill_label(shipment.tracking_id) # Label data will be retrieved from courier
        printable_strings.extend(shipment.get_printable_description()) # Merging courier data with system data
        return self.generate_pdf(printable_strings)

    def generate_pdf(self, lines: list) -> io.BytesIO:
        buffer = io.BytesIO()
        pdf_file = canvas.Canvas(buffer)
        y_position = 750
        for line in lines:
            pdf_file.drawString(30, y_position, line)
            y_position -= 20
        pdf_file.showPage()
        pdf_file.save()
        buffer.seek(0)
        return buffer
    
    def update_shipment_status(self, data: dict):
        assert 'status' in data, "New status should be provided"
        shipment = self.retrieve_shipment_by_identifiers(data)
        shipment_status = data['status']
        provider = shipment.provider
        courier = self.courier_factory.create_courier(provider)
        assert self.shipment_service.validate_shipment_status(shipment, courier, shipment_status), "Requested status is not supported by the system or the courier"
        shipment_status = courier.map_waybill_status(shipment_status)
        return self.shipment_service.create_update_shipment({
            'status': shipment_status
        }, shipment_model=shipment)

    def get_shipments(self, filters: dict):
        return self.shipment_service.get_shipments_by_filters(filters)

    def cancel_shipment(self, data: dict):
        shipment = self.retrieve_shipment_by_identifiers(data)
        provider = shipment.provider
        courier = self.courier_factory.create_courier(provider)
        assert isinstance(courier, CancellableCourier), "The courier doesn't support cancel operation"
        courier.cancel(shipment)
        return self.shipment_service.create_update_shipment({
            'status': Shipment.CANCELLED
        }, shipment_model=shipment)
    
    def retrieve_shipment_by_identifiers(self, data: dict):
        assert any(['id' in data, 'tracking_id' in data]), "Request should contain either id or tracking_id"
        if 'id' in data and data['id'] is not None:
            shipment = self.shipment_service.get_shipment_by_id(data['id'])
        else:
            shipment = self.shipment_service.get_shipment_by_tracking_id(data['tracking_id'])
        return shipment
