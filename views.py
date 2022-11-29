from Controller.ShipmentController import ShipmentController
from Services.CourierServices.SMSA import SMSA
from Services.ShipmentServices.ShipmentService import ShipmentService
from Services.CourierServices.CourierFactory import CourierFactory
from Services.CourierServices.CancellableCourier import CancellableCourier
from Serializers.ShipmentSerializer import ShipmentSerializer
from Serializers.UpdateShipmentSerializer import UpdateShipmentSerializerRequest
from shipapp.models import Shipment
from rest_framework.decorators import api_view, schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
import io
import logging
from reportlab.pdfgen import canvas
from django.http import FileResponse
from drf_spectacular.utils import (extend_schema, OpenApiExample, inline_serializer)

logger = logging.getLogger(__name__)

COURIERS_MAP = {
    'smsa': SMSA
}
shipment_service = ShipmentService()
courier_factory = CourierFactory()
controller = ShipmentController(shipment_service, courier_factory)


@extend_schema(
    request=ShipmentSerializer,
    responses=ShipmentSerializer
)
@api_view(['POST'])
def create_shipment(request):
    """Endpoint to create new shipment.

    Args:
        data (Shipment): Shipment data

    Returns:
        Shipment: The newly create shipment object
    """
    try:
        data = request.data
        result = controller.create_shipment(data)
        if not result['status']:
            return Response(result['errors'], status=status.HTTP_400_BAD_REQUEST)
        return Response(result['shipment'], status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.exception(f'Error happened during creating shipment: {e}')
        return Response({'status': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    request=UpdateShipmentSerializerRequest,
    responses=ShipmentSerializer
)
@api_view(['POST'])
def update_shipment_status(request):
    """Endpoint to update shipment status.
    It could be registered as a webhook to track shipment status

    Args:
        id (int): shipment id
        tracking_id (int): tracking id

    Returns:
        dict: Update shipment object
    """
    data = request.data
    return mutate_shipment_state(data, controller.update_shipment_status)

@extend_schema(
    request=UpdateShipmentSerializerRequest,
    responses=ShipmentSerializer
)
@api_view(['GET'])
def get_shipment(request):
    """Endpoint to get shipments details.

    Args:
        filters (dict): query param filters to be used to filter shipments

    Returns:
        List: List of shipments
    """
    filters = request.query_params.dict()
    data = controller.get_shipments(filters)
    return Response(data, status=status.HTTP_200_OK)

@extend_schema(
    request=UpdateShipmentSerializerRequest,
    responses=ShipmentSerializer
)
@api_view(['POST'])
def cancel_shipment(request):
    """Endpoint to cancel shipment.
    User can either provide id (shipment id) or tracking_id

    Args:
        id (int): shipment id
        tracking_id (int): tracking id

    Returns:
        dict: Update shipment object
    """
    data = request.data
    return mutate_shipment_state(data, controller.cancel_shipment)

@api_view(['GET'])
def print_label(request, id):
    """Endpoint to print shipment waybill label

    Args:
        id (int): Shipment id

    Returns:
        File: waybill label PDF
    """
    buffer = controller.print_waybill_label(id)
    return FileResponse(buffer, as_attachment=True, filename=f'{id}.pdf')

def mutate_shipment_state(data: dict, updater: callable) -> Response:
    try:
        result = updater(data)
        if not result['status']:
            return Response(result['errors'], status=status.HTTP_400_BAD_REQUEST)
        return Response(result['shipment'], status=status.HTTP_200_OK)
    except AssertionError as e:
        logger.exception(f'bad request: {e}')
        return Response({
            'status': 'error',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Shipment.DoesNotExist:
        logger.exception('Cannot find the requested shipment')
        return Response({'status': 'error'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.exception(f'Error happened during updating shipment: {e}')
        return Response({'status': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
