import os
import requests

from main import get_programs, format_slack

SLACK_URL = os.environ.get('SLACK_URL')


def notify_slack():
    programs = get_programs()
    payload = format_slack(programs)
    requests.post(SLACK_URL, payload)


if __name__ == "__main__":
    notify_slack()
