import requests

from .credits_calculator import CreditsCalculator
from api.models.credit_calculation_result import CreditCalculationResult


class ReportCreditsCalculator(CreditsCalculator):

    REPORTS_URL = 'https://owpublic.blob.core.windows.net/tech-task/reports/'

    def calculate(self, report_id) -> CreditCalculationResult:
        url = self.REPORTS_URL + str(report_id)
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return CreditCalculationResult(credits_used=data['credit_cost'], report_name=data['name'])
        else:
            raise Exception(f"Could not get credit cost for report with id {report_id}")

