import os
import json
import requests


URL = 'https://asia-northeast1-develop-187803.cloudfunctions.net/wnl_programs_api'
SLACK_URL = os.environ.get('SLACK_URL')


def notify_slack(request):
    res = requests.get(URL, params={'format': 'slack'})
    # print(res.url)  # for debug
    payload = res.json()
    payload.update(
        {
            'icon_emoji': ':rainbow:',
            'username': 'Weather News Live Programs Notification',
        }
    )
    res = requests.post(SLACK_URL, data=json.dumps(payload))
    # print(res.text)  # for debug
    return 'notified slack!'


if __name__ == "__main__":
    notify_slack(None)
