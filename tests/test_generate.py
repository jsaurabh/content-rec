import unittest
from data.generate import argument_parser, extract_datacamp, run

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = argument_parser()
    
    def test_parser(self):
        parsed = self.parser.parse_args(["--file", "url.txt", "--out", "data.csv", "--lang", "R"])
        self.assertEqual(parsed.file, "url.txt")
        self.assertEqual(parsed.out, "data.csv")
        self.assertEqual(parsed.lang, "R")

    def test_dom_extraction(self):
        test_url = "https://www.datacamp.com/courses/intro-to-python-for-data-science"
        test_answer = {}
        self.assertEqual(extract_datacamp(test_url), test_answer)

        test_url = "https://www.datacamp.com/courses/natural-language-generation-in-python"
        test_answer = {
            'title': 'Natural Language Generation in Python',
<<<<<<< HEAD
            'short_description': 'Learn to generate language in Python using Deep Learning in Python.',
            'long_description': "Have you ever wondered how Gmail autocompletes your sentences, or, what powers the WhatsApp suggestions when you’re typing a message? The technology behind these helpful writing hints is machine learning. In this course, you'll build and train machine learning models for different natural language generation tasks. For example, you'll train a model on the literary works of Shakespeare and generate text in the style of his writing. You'll also learn how to create a neural translation model to translate English sentences into French. Finally, you'll train a seq2seq model to generate your own natural language autocomplete sentences, just like Gmail!",  # noqa: E501
=======
            'description': "Have you ever wondered how Gmail autocompletes your sentences, or, what powers the WhatsApp suggestions when you’re typing a message? The technology behind these helpful writing hints is machine learning. In this course, you'll build and train machine learning models for different natural language generation tasks. For example, you'll train a model on the literary works of Shakespeare and generate text in the style of his writing. You'll also learn how to create a neural translation model to translate English sentences into French. Finally, you'll train a seq2seq model to generate your own natural language autocomplete sentences, just like Gmail!",  # noqa: E501
>>>>>>> 5dc7f185674913408ad9c1118f1598371c1e648c
            'provider': 'DataCamp',
            'url': 'https://www.datacamp.com/courses/natural-language-generation-in-python',
            'time': '4 hours',
            'language': 'Python',
            'paths': 'Deep Learning for NLP in Python',
            'prerequisites': 'Introduction to Natural Language Processing in Python,Advanced Deep Learning with Keras',  # noqa: E501
            'medium': 'video',
            'type': 'course'
        }
        self.assertEqual(extract_datacamp(test_url, lang="Python", medium="video",
                                          _type="course"), test_answer)

        self.assertNotEqual(extract_datacamp(test_url), test_answer)

    def test_runner(self):
        parsed = self.parser.parse_args(["--file", "urls.txt", "--out", "dataset.csv",
                                         "--lang", "Python"])
        results = run(parsed)

        with open(parsed.file) as f:
            data = f.readlines()
        
        outlen = len(data)
        assert type(results) == list, "Output return type unexpected. Expected list"
        assert len(results) == outlen, "Output list length not correponding to input length"