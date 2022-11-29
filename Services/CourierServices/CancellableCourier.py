import abc
from shipapp.models import Shipment
  
class CancellableCourier(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def cancel(self, shipment: Shipment) -> bool:
        '''
        An abstract function that should be implemented by clients
        to cancel a shipment request
        '''
        pass
