from django.test import TestCase

from fe_azure.queue import send_tag
from instagram.models import Tag


class TestSendTag(TestCase):

    def test_send_tag__love_does_not_exists(self):
        assert Tag.objects.filter(name='love').count() == 0
        send_tag('love')
        assert Tag.objects.filter(name='love').count() > 0
