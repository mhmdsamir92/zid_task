from django.db import models
from django.core.validators import MinValueValidator, EmailValidator

class Shipment(models.Model):

    ARAMEX = "ARAMEX"
    SMSA = "SMSA"
    SHIPBOX = "SHIPBOX"
    
    PROVIDER_CHOICES = (
        (ARAMEX, ARAMEX),
        (SMSA, SMSA),
        (SHIPBOX, SHIPBOX),
    )

    REGISTERED = "REGISTERED"
    PENDING = "PENDING"
    TRANSIT = "TRANSIT"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

    SYSTEM_STATUS = (
        (REGISTERED, REGISTERED), # Shipment is registered in the system and will be sent to one of the couriers soon
        (PENDING, PENDING), # Shipment is sent to one of the courier and it's currently pending to track
        (TRANSIT, TRANSIT), # Shipment is on the way to the receiver
        (DELIVERED, DELIVERED), # Shipment is delivered
        (FAILED, FAILED), # Shipment is failed to be delivered
        (CANCELLED, CANCELLED) # Shipment is cancelled
    )

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    length = models.FloatField(validators=[MinValueValidator(0.1)])
    width = models.FloatField(validators=[MinValueValidator(0.1)])
    height = models.FloatField(validators=[MinValueValidator(0.1)])
    weight = models.FloatField(validators=[MinValueValidator(0.1)])
    number_of_pieces = models.IntegerField(validators=[MinValueValidator(1)])
    product_country = models.CharField(max_length=50)
    sender_name = models.CharField(max_length=200)
    sender_mobile = models.CharField(max_length=50)
    sender_email = models.CharField(max_length=200, validators=[EmailValidator()])
    sender_full_address = models.CharField(max_length=300)
    sender_country = models.CharField(max_length=50)
    receiver_name = models.CharField(max_length=200)
    receiver_mobile = models.CharField(max_length=50)
    receiver_email = models.CharField(max_length=200, validators=[EmailValidator()])
    receiver_full_address = models.CharField(max_length=300)
    receiver_country = models.CharField(max_length=50)
    shipping_date = models.DateTimeField()
    tracking_id = models.CharField(max_length=200, null=True, unique=True)
    status = models.CharField(max_length=50, choices=SYSTEM_STATUS, default=REGISTERED)
    created_at = models.DateTimeField(auto_now=True)

    def get_printable_description(self):
        return [
            f'Shipment title: {self.title}',
            f'Shipment description: {self.description}',
            f'Shipment provider (courier): {self.provider}',
            f'Shipment length: {self.length}',
            f'Shipment width: {self.width}',
            f'Shipment height: {self.height}',
            f'Shipment status: {self.status}',
            f'Number of pieces: {self.number_of_pieces}',
            f'Product country: {self.product_country}',
            f'Sender name: {self.sender_name}',
            f'Sender mobile: {self.sender_mobile}',
            f'Sender email: {self.sender_email}',
            f'Sender full address: {self.sender_full_address}',
            f'Sender country: {self.sender_country}',
            f'Receiver name: {self.receiver_name}',
            f'Receiver mobile: {self.receiver_mobile}',
            f'Receiver email: {self.receiver_email}',
            f'Receiver full address: {self.receiver_full_address}',
            f'Receiver country: {self.receiver_country}',
            f'Shipping date: {self.shipping_date}',
            f'Tracking id: {self.tracking_id}',
            
        ]

