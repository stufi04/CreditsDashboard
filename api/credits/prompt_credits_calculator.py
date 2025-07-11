import re
from api.models.credit_calculation_result import CreditCalculationResult
from .credits_calculator import CreditsCalculator


class PromptCreditsCalculator(CreditsCalculator):

    BASE_COST = 1

    def __init__(self):
        self.words = None

    def calculate(self, prompt) -> CreditCalculationResult:
        self.words = self.extract_words(prompt)

        total_credits = self.BASE_COST
        total_credits += PromptCreditsCalculator.character_cost(prompt)
        total_credits += self.word_length_cost()
        total_credits += PromptCreditsCalculator.third_vowel_cost(prompt)
        total_credits += PromptCreditsCalculator.length_penalty(prompt)
        total_credits += self.unique_word_bonus()

        total_credits = max(total_credits, 1)

        if PromptCreditsCalculator.is_palindrome(prompt):
            total_credits *= 2

        return CreditCalculationResult(credits_used=round(total_credits, 2))

    def word_length_cost(self):
        if not self.words:
            return 0
        cost = 0
        for word in self.words:
            length = len(word)
            if length <= 3:
                cost += 0.1
            elif 4 <= length <= 7:
                cost += 0.2
            else:
                cost += 0.3
        return cost

    def unique_word_bonus(self):
        if not self.words:
            return 0
        return -2 if len(set(self.words)) == len(self.words) and self.words else 0

    @staticmethod
    def character_cost(text):
        return 0.05 * len(text)

    @staticmethod
    def third_vowel_cost(text):
        vowels = set('aeiouAEIOU')
        return 0.3 * sum(1 for i in range(2, len(text), 3) if text[i] in vowels)

    @staticmethod
    def length_penalty(text):
        return 5 if len(text) > 100 else 0

    @staticmethod
    def is_palindrome(text):
        if text == "":
            return False
        normalized = re.sub(r'[^a-zA-Z0-9]', '', text).lower()
        return normalized == normalized[::-1]

    @staticmethod
    def extract_words(text):
        return re.findall(r"[a-zA-Z'-]+", text)