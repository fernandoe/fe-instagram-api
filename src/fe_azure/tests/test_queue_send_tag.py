from unittest.mock import patch

from django.test import TestCase

from fe_azure.queue import send_tag
from instagram.models import Tag


class TestSendTag(TestCase):

    def test_send_tag__none(self):
        assert Tag.objects.all().count() == 0
        send_tag(None)
        assert Tag.objects.filter(name='love').count() == 0

    def test_send_tag__blank(self):
        assert Tag.objects.all().count() == 0
        send_tag('')
        assert Tag.objects.filter(name='love').count() == 0

    def test_send_tag__love_does_not_exists(self):
        love = 'love'
        assert Tag.objects.filter(name=love).count() == 0
        send_tag(love)
        tag = Tag.objects.first()
        assert tag.name == love
        assert tag.last_count is None
        assert tag.languages is None

    def test_send_tag__love_exists(self):
        love = 'love'
        tag = Tag.objects.create(name=love)
        send_tag(tag.name)
        tag.refresh_from_db()
        assert tag.name == love
        assert tag.last_count is None
        assert tag.languages is None
