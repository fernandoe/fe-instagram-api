from django.test import TestCase

from instagram.helpers import is_valid_tag


class TestIsValidTag(TestCase):

    def test_valid_tag_with_letters_and_numbers(self):
        assert is_valid_tag('#ab12cd')

    def test_valid_tag_with_numbers_in_the_end(self):
        assert is_valid_tag('#abc12')

    def test_valid_tag_with_numbers_in_the_middle(self):
        assert is_valid_tag('#ab1c')

    def test_invalid_tag_with_two_hashes(self):
        assert not is_valid_tag('#abc#123')

    def test_invalid_tag_none(self):
        assert not is_valid_tag(None)

    def test_invalid_tag(self):
        assert not is_valid_tag('#incredibleindia🇮🇳')

    def test_invalid_chinese(self):
        assert not is_valid_tag('#12筋')

    def test_invalid_keolcheodei(self):
        assert not is_valid_tag('#필름감성')

    def test_invalid_more_than_100_chars(self):
        assert not is_valid_tag("#%s" % ('a' * 101))
