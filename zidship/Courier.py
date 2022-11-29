import abc
  
class AbstractClass(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def abstractName(self):
        pass
  
class ValidSubClass(AbstractClass):
    def abstractName(self):
        return 'Abstract 1'

def myFun(param: str):
	print("hi")