import pytest
import datetime


@pytest.fixture
def programs():
    return [
        {
            'start_dt': datetime.datetime(2019, 4, 16, 20, 0),
            'title': 'ウェザーニュースLiVE・ムーン',
            'caster': '松雪彩花（あやち）',
        },
        {
            'start_dt': datetime.datetime(2019, 4, 16, 23, 0),
            'title': 'ウェザーニュースLiVE',
            'caster': '無人',
        },
        {
            'start_dt': datetime.datetime(2019, 4, 17, 0, 0),
            'title': 'ウェザーニュースLiVE',
            'caster': '無人',
        },
        {
            'start_dt': datetime.datetime(2019, 4, 17, 5, 0),
            'title': 'ウェザーニュースLiVE・モーニング',
            'caster': '角田奈緒子（なおちゃん）',
        },
        {
            'start_dt': datetime.datetime(2019, 4, 17, 8, 0),
            'title': 'ウェザーニュースLiVE・サンシャイン',
            'caster': '江川清音（さーやん）',
        },
        {
            'start_dt': datetime.datetime(2019, 4, 17, 11, 0),
            'title': 'ウェザーニュースLiVE・コーヒータイム',
            'caster': '鈴木里奈（りなっち）',
        },
        {
            'start_dt': datetime.datetime(2019, 4, 17, 14, 0),
            'title': 'ウェザーニュースLiVE・アフタヌーン',
            'caster': '檜山沙耶（さやっち）',
        },
        {
            'start_dt': datetime.datetime(2019, 4, 17, 17, 0),
            'title': 'ウェザーニュースLiVE・イブニング',
            'caster': '駒木結衣（ゆいちゃん）',
        },
        {
            'start_dt': datetime.datetime(2019, 4, 17, 20, 0),
            'title': 'ウェザーニュースLiVE・ムーン',
            'caster': '白井ゆかり（ゆかりん）',
        },
        {
            'start_dt': datetime.datetime(2019, 4, 17, 23, 0),
            'title': 'ウェザーニュースLiVE',
            'caster': '無人',
        },
    ]
