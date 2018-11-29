import json
import os
import uuid

import requests

subscriptionKey = os.getenv('FE_AZURE_TRANSLATOR_KEY')

base_url = 'https://api.cognitive.microsofttranslator.com'
path = '/detect?api-version=3.0'
constructed_url = base_url + path

headers = {
    'Ocp-Apim-Subscription-Key': subscriptionKey,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}


def detect(word):
    body = [{'text': word}]
    request = requests.post(constructed_url, headers=headers, json=body)
    response_data = request.json()
    print(json.dumps(response_data, sort_keys=True, indent=4, ensure_ascii=False, separators=(',', ': ')))
    langs = []
    if len(response_data) > 0:
        for data in response_data:
            if 'language' in data:
                langs.append(data['language'])
            if 'alternatives' in data:
                for lang in data['alternatives']:
                    langs.append(lang['language'])
    return langs
