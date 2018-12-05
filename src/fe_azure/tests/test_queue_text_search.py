from django.test import TestCase

from instagram.models import TextSearch
from instagram.views import search_impl


class TestTextSearch(TestCase):

    def test_send_text_search_love(self):
        assert TextSearch.objects.all() == 0
        search_impl('love', '30')
        assert TextSearch.objects.all() == 1
