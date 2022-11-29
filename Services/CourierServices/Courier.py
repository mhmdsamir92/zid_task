import abc
  
class Courier(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def create_waybill(self, data: dict) -> str:
        '''
        An abstract function that should be implemented by clients
        to create a waybill and return tracking id
        '''
        pass

    @abc.abstractmethod
    def get_waybill_label(self, tracking_id: int) -> list:
        '''
        An abstract function that should be implemented by clients
        to get waybill label given tracking id
        '''
        pass

    @abc.abstractmethod
    def retrieve_waybill_status(self) -> list:
        '''
        An abstract function that should be implemented by clients
        to retrieve courier possible statuses
        '''
        pass

    def is_status_existed(self, status: str) -> bool:
        return status in self.retrieve_waybill_status()

    def map_waybill_status(self, status: str) -> str:
        return self.retrieve_waybill_status()[status]
