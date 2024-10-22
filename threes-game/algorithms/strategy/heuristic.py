from abc import ABC, abstractmethod


class Heuristic(ABC):
    """
    Abstract base class for heuristic evaluation.

    This class serves as a blueprint for creating heuristic algorithms that
    evaluate a given state. Subclasses must implement the evaluate method.

    Methods:
        evaluate(state): Abstract method to evaluate a given state.
    """

    @abstractmethod
    def evaluate(self, state):
        """
        Abstract method to evaluate a given state.

        Subclasses must implement this method to provide specific evaluation
        logic for the state.

        Args:
            state: The state to be evaluated.
        """
        pass
