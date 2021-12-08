import requests
import json

url = 'https://hooks.slack.com/services/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'

def post_message(message):
    payload = {
        'text': message
    }
    r = requests.post(url, json=payload)
    print(r.text)
    if r.status_code > 200:
        print('Error posting to Slack!')
