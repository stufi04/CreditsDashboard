import requests
from flask import jsonify

from .prompt_credits_calculator import PromptCreditsCalculator
from .report_credits_calculator import ReportCreditsCalculator
from api.models.credit_calculation_result import CreditCalculationResult
from api.models.message import Message


class CreditsService:

    MESSAGES_URL = 'https://owpublic.blob.core.windows.net/tech-task/messages/current-period'

    def __init__(self):
        self.promptCreditsCalculator = PromptCreditsCalculator()
        self.reportCreditsCalculator = ReportCreditsCalculator()

    def get_usage(self):
        response = requests.get(self.MESSAGES_URL)

        if response.status_code == 200:
            data = response.json()
            usage = self.process_messages(data['messages'])
            return jsonify([m.to_dict() for m in usage])
        else:
            print(f"Error: {response.status_code}")

    def process_messages(self, data):
        usage = []
        for message in data:
            credit_calculation_result = self.get_credits(message)
            result = Message(
                        message['id'],
                        message['timestamp'],
                        credit_calculation_result.credits_used,
                        credit_calculation_result.report_name
            )
            usage.append(result)
        return usage

    def get_credits(self, data_point) -> CreditCalculationResult:
        if 'report_id' in data_point:
            try:
                return self.reportCreditsCalculator.calculate(data_point['report_id'])
            except Exception as e:
                print(f"ReportCreditsCalculator failed: {e}")
                return self.promptCreditsCalculator.calculate(data_point['text'])
        else:
            return self.promptCreditsCalculator.calculate(data_point['text'])

