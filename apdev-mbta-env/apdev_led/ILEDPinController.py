from abc import ABC, abstractmethod

class ILEDPinController(ABC):

    @abstractmethod
    def get_is_lit(self) -> bool:
        pass

    @abstractmethod
    def set_is_lit(self, is_lit:bool):
        pass

    @abstractmethod
    def toggle_is_lit(self) -> bool:
        pass