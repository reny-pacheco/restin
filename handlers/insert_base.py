from abc import ABC, abstractmethod


class InsertBase(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def insert_data(self):
        pass

    @abstractmethod
    def close(self):
        pass
