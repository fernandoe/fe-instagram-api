from django.test import TestCase

from instagram.helpers import extract_count


class TestExtractCount(TestCase):

    def test_with_like(self):
        count = extract_count('like')
        assert count is None
