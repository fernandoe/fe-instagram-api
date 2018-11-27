from django.test import TestCase

from instagram.helpers import filter_tag


class TestFilterTag(TestCase):

    def test_valid_word(self):
        assert filter_tag('#incredibleindia')

    def test_valid_word_with_numbers_in_the_end(self):
        assert filter_tag('#abc1')

    def test_valid_word_with_numbers_in_the_middle(self):
        assert filter_tag('#ab1c')

    def test_invalid_word(self):
        assert not filter_tag('#incredibleindia🇮🇳')

    def test_invalid_chinese(self):
        assert filter_tag('#筋トレ')
