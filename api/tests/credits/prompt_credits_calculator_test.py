import unittest
from api.credits.prompt_credits_calculator import PromptCreditsCalculator
from api.models.credit_calculation_result import CreditCalculationResult

class TestPromptCreditsCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = PromptCreditsCalculator()

    def test_extract_words(self):
        text = "I'm testing prompt-based words like well-being. It's cool."
        expected = ["I'm", 'testing', 'prompt-based', 'words', 'like', 'well-being', "It's", "cool"]
        self.assertEqual(self.calculator.extract_words(text), expected)

    def test_word_length_cost(self):
        self.calculator.words = ["hi", "word", "elephant"]
        self.assertEqual(self.calculator.word_length_cost(), 0.1 + 0.2 + 0.3)

    def test_word_length_cost_when_words_is_none(self):
        calculator = PromptCreditsCalculator()
        self.assertEqual(calculator.word_length_cost(), 0)

    def test_unique_word_bonus_unique(self):
        self.calculator.words = ["one", "two", "three"]
        self.assertEqual(self.calculator.unique_word_bonus(), -2)

    def test_unique_word_bonus_case_sensitive(self):
        self.calculator.words = ["one", "two", "One", "TWO"]
        self.assertEqual(self.calculator.unique_word_bonus(), -2)

    def test_unique_word_bonus_duplicate(self):
        self.calculator.words = ["one", "two", "two"]
        self.assertEqual(self.calculator.unique_word_bonus(), 0)

    def test_unique_word_bonus_when_words_is_none(self):
        calculator = PromptCreditsCalculator()
        self.assertEqual(calculator.unique_word_bonus(), 0)

    def test_character_cost(self):
        self.assertEqual(self.calculator.character_cost("hello"), 0.05 * 5)
        self.assertEqual(self.calculator.character_cost("hi"), 0.05 * 2)
        self.assertEqual(self.calculator.character_cost(""), 0)
        self.assertEqual(self.calculator.character_cost("a" * 100), 5)

    def test_third_vowel_cost(self):
        self.assertEqual(self.calculator.third_vowel_cost("abecidofu"), 0.6)
        self.assertEqual(self.calculator.third_vowel_cost("abe"), 0.3)
        self.assertEqual(self.calculator.third_vowel_cost("abc"), 0)
        self.assertEqual(self.calculator.third_vowel_cost("ABCDEFGHIJKLMN"), 0.3)

    def test_length_penalty(self):
        short_text = "a" * 100
        long_text = "b" * 101
        self.assertEqual(self.calculator.length_penalty(short_text), 0)
        self.assertEqual(self.calculator.length_penalty(long_text), 5)

    def test_is_palindrome_true(self):
        text = "A man, a plan, a canal: Panama"
        self.assertTrue(self.calculator.is_palindrome(text))

    def test_is_palindrome_false(self):
        text = "This is not a palindrome"
        self.assertFalse(self.calculator.is_palindrome(text))

    def test_calculate_defaults_to_one(self):
        prompt = "hello world"
        result = self.calculator.calculate(prompt)
        self.assertIsInstance(result, CreditCalculationResult)
        # base count: 1
        # character counts: 11 * 0.05 = 0.55
        # word len multipliers: 2 * 0.2 = 0.4
        # third vowels: 0
        # length penalty: 0
        # unique bonus: -2
        # not a palindrome
        # total: 1.95 - 2 => default to minimum 1
        self.assertEqual(result.credits_used, 1)

    def test_calculate_basic_example(self):
        prompt = "this is an example prompt"
        result = self.calculator.calculate(prompt)
        self.assertIsInstance(result, CreditCalculationResult)
        # base count: 1
        # character counts: len * 0.05
        # word len multipliers: 2 * 0.1 + 3 * 0.2 = 0.8
        # third vowels: 5 * 0.3 = 1.5
        # length penalty: 0
        # unique bonus: -2
        # not a palindrome
        self.assertEqual(result.credits_used, 1 + len(prompt) * 0.05 + 0.8 + 1.5 - 2)

    def test_calculate_with_duplicate_words(self):
        prompt = "we are who we are"
        result = self.calculator.calculate(prompt)
        self.assertIsInstance(result, CreditCalculationResult)
        # base count: 1
        # character counts: len * 0.05
        # word len multipliers: 5 * 0.1 = 0.5
        # third vowels: 2 * 0.3 = 0.6
        # length penalty: 0
        # unique bonus: 0
        # not a palindrome
        self.assertEqual(result.credits_used, 1 + len(prompt) * 0.05 + 0.5 + 0.6)

    def test_calculate_palindrome_bonus(self):
        prompt = "Was it a car or a cat I saw"
        result = self.calculator.calculate(prompt)
        self.assertIsInstance(result, CreditCalculationResult)
        # base count: 1
        # character counts: len * 0.05
        # word len multipliers: 9 * 0.1 = 0.9
        # third vowels: 0
        # length penalty: 0
        # unique bonus: 0
        # double for palindrom
        self.assertEqual(result.credits_used, 2 * (1 + len(prompt) * 0.05 + 0.9))

    def test_empty_string(self):
        prompt = ""
        result = self.calculator.calculate(prompt)
        self.assertIsInstance(result, CreditCalculationResult)
        self.assertEqual(result.credits_used, 1)

if __name__ == "__main__":
    unittest.main()