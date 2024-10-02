from abc import ABC, abstractmethod

class SearchAlgorithm(ABC):
    
    @abstractmethod
    def get_next_move(self):
        pass