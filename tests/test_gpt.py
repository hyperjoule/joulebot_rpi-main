import unittest
from gpt import ask_gpt

class TestGPT(unittest.TestCase):

    def test_ask_gpt_successful(self):
        # Replace this with a question you want to test
        test_question = "What's the capital of France?"

        response = ask_gpt(test_question)

        # Check if the response is not the error message
        self.assertNotEqual(response, "I'm sorry, but I'm having trouble connecting right now. Please try again later.")

if __name__ == '__main__':
    unittest.main()