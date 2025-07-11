from abc import ABC, abstractmethod

from api.models.credit_calculation_result import CreditCalculationResult


class CreditsCalculator(ABC):

    @abstractmethod
    def calculate(self, data) -> CreditCalculationResult:
        pass