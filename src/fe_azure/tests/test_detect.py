from unittest import TestCase

from fe_azure.translate import detect


class TestDetect(TestCase):

    def test_detect_valid_word_casa(self):
        langs = detect('casa')
        assert 3 == len(langs)
        assert 'it' in langs
        assert 'es' in langs
        assert 'pt' in langs

    def test_detect_valid_word_18anos(self):
        langs = detect('18anos')
        assert 3 == len(langs)
        assert 'pt' in langs
        assert 'en' in langs
        assert 'es' in langs

    def test_detect_valid_word_academiabox198(self):
        langs = detect('academiabox198')
        assert 3 == len(langs)
        assert 'en' in langs
        assert 'de' in langs
        assert 'fr' in langs
