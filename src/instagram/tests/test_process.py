from django.test import TestCase
import pytest
from instagram.management.commands.job_extract_posts_from_hashtag import process


class TestProcess(TestCase):

    @pytest.mark.django_db
    def test_process(self):
        process('duda')
