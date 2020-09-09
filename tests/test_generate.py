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
            'description': 'Learn to generate language in Python using Deep Learning in Python.',
            'provider': 'DataCamp',
            'url': 'https://www.datacamp.com/courses/natural-language-generation-in-python',
            'time': '4 hours',
            'language': 'Python',
            'paths': 'Deep Learning for NLP in Python',
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