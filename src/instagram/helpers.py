import re


def filter_tag(word):
    hashtag_re = re.compile("(?:^|\s)[＃#]{1}(\w+)$")
    if hashtag_re.match(word):
        return True
    else:
        print(f"Inválido: {word}")
        return False
