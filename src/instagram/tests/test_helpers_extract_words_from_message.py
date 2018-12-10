from django.test import TestCase

from instagram.helpers import extract_words_from_message


class TestSaveTag(TestCase):
    def test_extract_words_from_message__is_valid(self):
        tags = extract_words_from_message('alou #abc #ldld')
        assert 'alou' in tags
        assert '#abc' in tags
        assert '#ldld' in tags

    def test_extract_words_from_message__is_invalid_with_bytes(self):
        tags = extract_words_from_message(b'alou #abc #ldld')
        assert 'alou' in tags
        assert '#abc' in tags
        assert '#ldld' in tags
