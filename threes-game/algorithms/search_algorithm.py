from abc import ABC, abstractmethod

class SearchAlgorithm(ABC):
    """Abstract base class for search algorithms."""

    @abstractmethod
    def get_next_move(self):
        """
        Abstract method to get the next move in the search process.

        :return: The next move.
        """
        pass
