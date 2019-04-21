import pytest
import os
import json
import datetime
import freezegun
from requests_html import HTMLSession
from requests_file import FileAdapter


from src.main import get_programs


session = HTMLSession()
session.mount('file://', FileAdapter())


def get():
    '''
    from
    https://github.com/kennethreitz/requests-html/blob/master/tests/test_requests_html.py
    '''
    path = os.path.sep.join((os.path.dirname(os.path.abspath(__file__)), 'test.html'))
    url = 'file://{}'.format(path)

    return session.get(url)


@freezegun.freeze_time('2019-04-16 21:00:00')
def test_get_programs(mocker, programs):
    mocker.patch('src.main._fetch_wni', return_value=get().html)
    _programs = get_programs()
    for _p, expected in zip(_programs, programs):
        assert _p['caster'] == expected['caster']
        assert _p['title'] == expected['title']
        assert _p['start_dt'].strftime('%Y%m%d%H%M%S') == expected['start_dt'].strftime(
            '%Y%m%d%H%M%S'
        )
