import json
import re

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from instagram.models import Tag, Post


class Command(BaseCommand):


    def handle(self, *args, **options):
        posts = Post.objects.all()
        for post in posts:
            print(f"Processing: {post}")
            post.indexing()
