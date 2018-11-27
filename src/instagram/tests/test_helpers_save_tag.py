# from django.test import TestCase
#
# from instagram.helpers import save_tag
#
#
# class TestSaveTag(TestCase):
#
#     def test_invalid_tag_none(self):
#         from instagram.models import Tag
#         assert save_tag(None)
#         assert Tag.objects.all().count() == 0
#
#     def test_invalid_tag_without_hash(self):
#         from instagram.models import Tag
#         assert save_tag('abc')
#         assert Tag.objects.all().count() == 0
#
#     def test_valid_tag_with_hash(self):
#         from instagram.models import Tag
#         assert save_tag('#abc')
#         assert Tag.objects.get(name='abc')
