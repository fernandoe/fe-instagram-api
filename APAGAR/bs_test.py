import json
import requests
from bs4 import BeautifulSoup

def do():
    r = requests.get('https://www.instagram.com/explore/tags/nature/')
    soup = BeautifulSoup(r.text, 'lxml')

    script = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
    page_json = script.text.split(' = ', 1)[1].rstrip(';')
    data = json.loads(page_json)

    for post in data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
        # image_src = post['node']['thumbnail_resources'][1]['src']
        # print(image_src)
        print('=' * 100)
        print(post)

    # page = requests.get("https://www.instagram.com/explore/tags/cute/")
    # soup = BeautifulSoup(page.text, 'html.parser')
    # all_div_a = soup.find_all('h2')
    # print(all_div_a)

    # print(soup.prettify())
    # print(title)
    # >> 'title'? Python For Beginners
    # print soup.title.string
    # >> ? Python For Beginners
    # print soup.p
    # print soup.a
    # Python For Beginners

if __name__ == '__main__':
    do()
