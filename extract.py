import os

import requests

BASE_URL = "https://api.instagram.com/v1/tags/"
ACCESS_TOKEN = os.environ.get("INSTAGRAM_ACCESS_TOKEN")


def do():
    tags = extract_tags('tags.txt')
    tags_new = set(extract_tags('tags_new.txt'))

    file_output = open("output.txt", "w+")

    for tag in tags:
        line = f"{tag},{get_count(tag)}\n"
        file_output.write(line)

    for tag in tags_new:
        if tag not in tags:
            line = f"{tag},{get_count(tag)}\n"
            file_output.write(line)

    file_output.close()


def get_count(tag):
    if tag.startswith('#'):
        tag = tag[1:]
    url = f"{BASE_URL}{tag}?access_token={ACCESS_TOKEN}"
    print(f"Tag: {tag}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: {response.content}")
    data = response.json()
    media_count = data['data']['media_count']
    return media_count


def extract_tags(file_name):
    file_tags = open(file_name, "r")
    result = []
    for tag in file_tags:
        result.append(tag.strip().lower())
    file_tags.close()
    return result


if __name__ == '__main__':
    do()
