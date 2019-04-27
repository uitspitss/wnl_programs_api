import os
import requests


URL = 'https://asia-northeast1-develop-187803.cloudfunctions.net/wnl_programs_api'
SLACK_URL = os.environ.get('SLACK_URL')


def notify_slack():
    res = requests.get(URL, params={'format': 'slack'})
    # print(res.url)  # for debug
    res = requests.post(SLACK_URL, res.text)
    # print(res.text)  # for debug


if __name__ == "__main__":
    notify_slack()
