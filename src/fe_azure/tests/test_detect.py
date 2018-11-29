from unittest import TestCase

from fe_azure.translate import detect


class TestDetect(TestCase):

    def test_detect_valid_word_casa(self):
        langs = detect('casa')
        assert 3 == len(langs)
        assert 'it' in langs
        assert 'es' in langs
        assert 'pt' in langs
