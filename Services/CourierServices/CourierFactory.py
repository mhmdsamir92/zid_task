from .Courier import Courier
from .SMSA import SMSA
from .Aramex import Aramex
from .ShipBox import ShipBox

class CourierFactory:
	COURIERS_MAP = {
		"smsa": SMSA,
		"aramex": Aramex,
		"shipbox": ShipBox
	}
	def create_courier(self, courier: str) -> Courier:
		return self.COURIERS_MAP[courier.lower()]()