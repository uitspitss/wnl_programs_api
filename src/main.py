import os
import re
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify, send_file
from google.cloud import storage
from requests_html import AsyncHTMLSession


API_KEY = os.environ.get('API_KEY')
CLOUD_STORAGE_BUCKET = os.environ.get('CLOUD_STORAGE_BUCKET')
CACHE_FILENAME = 'programs_cache.json'
SS_FILENAME = 'programs_ss.png'
SS_FILEPATH = f'/tmp/{SS_FILENAME}'

URL = 'https://weathernews.jp/s/solive24/timetable.html'
JST = timezone(timedelta(hours=+9), 'JST')
CASTER = {
    'noimage': '無人',
    'ailin': '山岸愛梨（あいりん）',
    'sayane': '江川清音（さーやん）',
    'izumin': '眞家泉（いずみん）',
    'matsu': '松雪彩花（あやち）',
    'shirai': '白井ゆかり（ゆかりん）',
    'takayama': '高山奈々（ななちゃん）',
    'nao': '角田奈緒子（なおちゃん）',
    'rina': '鈴木里奈（りなっち）',
    'hiyama': '檜山沙耶（さやっち）',
    'komaki': '駒木結衣（ゆいちゃん）',
    'airi': 'ウェザーロイド Airi',
}
COLORS = [
    '#26294a',
    '#01545a',
    '#017351',
    '#03c383',
    '#aad962',
    '#fbbf45',
    '#ef6a32',
    '#ed0345',
    '#a12a5e',
    '#710162',
]


def _fetch_wni():
    asession = AsyncHTMLSession()

    async def _fetch():
        r = await asession.get(URL)
        await r.html.arender(
            sleep=5,
            keep_page=True,
            script="document.getElementsByTagName('header')[0].remove();document.querySelector('p.pan').remove();",
        )
        clip = await r.html.page.evaluate(
            '''() => {
                const rect = document.getElementById('main').getBoundingClientRect();
                return {
                    x: 0,
                    y: 0,
                    width: rect.width,
                    height: rect.height
                };
            }'''
        )
        await r.html.page.screenshot({'path': SS_FILEPATH, 'clip': clip})
        return r

    r = asession.run(_fetch)[0]
    return r.html


def _get_programs() -> list:
    programs = []
    now = datetime.now(tz=JST)

    _dt_h = 0
    html = _fetch_wni()
    for li in html.xpath('//article[@id="main"]/section/ul/li'):
        dt_text = li.xpath('//span[@class="time"]')[0].text
        dt_h, _ = [int(x) for x in dt_text.split(':')]
        title = li.xpath('//span[@class="title"]')[0].text
        title = re.search(r'[\w・]+', title)[0]
        caster_jpg = li.xpath('//span[@class="caster"]/img')[0].attrs['src']
        caster_text = re.search(r'/([a-z]+?)((\d)*_\w+)*.jpg$$', caster_jpg)[1]

        if dt_h == 23 and caster_text == 'noimage':
            caster_text = 'airi'

        if _dt_h > dt_h:
            now += timedelta(days=1)

        programs.append(
            {
                'start_dt': datetime(
                    now.year, now.month, now.day, dt_h, 0, 0, tzinfo=JST
                ),
                'title': title,
                'caster': CASTER[caster_text],
            }
        )
        _dt_h = dt_h

    return programs


def _convert_dt(programs: list, to_str=True) -> list:
    formatted = []
    for p in programs:
        if to_str is True:
            p.update({'start_dt': f"{p['start_dt']:%Y-%m-%d %H:%M:%S%z}"})
        else:
            p.update(
                {'start_dt': datetime.strptime(p['start_dt'], '%Y-%m-%d %H:%M:%S%z')}
            )
        formatted.append(p)
    return formatted


def _format_slack(programs: list) -> dict:
    template_dict = {
        "attachments": [{"color": "", "title": f"今後の放送予定", "title_link": URL, "ts": 0}]
    }

    colors = COLORS[: len(programs)]
    for p, c in zip(programs, colors):
        template_dict['attachments'].append(
            {
                "color": c,
                "title": f"{p['start_dt']:%m/%d %H:%M}~ {p['title']}",
                "fields": [{'title': p['caster'], 'short': False}],
                "ts": 0,
            }
        )

    return template_dict


def _get_bucket():
    gcs = storage.Client()
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)
    return bucket


def _get_programs_from_cache():
    bucket = _get_bucket()
    blob = bucket.get_blob(CACHE_FILENAME)
    text = blob.download_as_string()
    return json.loads(text)


def _get_programs_ss_from_cache():
    bucket = _get_bucket()
    blob = bucket.get_blob(SS_FILENAME)
    blob.download_to_filename(SS_FILEPATH)
    return SS_FILEPATH


def update_programs_cache(request):
    if request is None or (
        request.method == 'POST'
        and json.loads(request.data.decode('utf-8')).get('API_KEY') == API_KEY
    ):
        programs = _get_programs()
        converted = _convert_dt(programs, to_str=True)

        bucket = _get_bucket()
        blob = bucket.blob(CACHE_FILENAME)
        blob.upload_from_string(json.dumps(converted), content_type='text/json')

        blob = bucket.blob(SS_FILENAME)
        blob.upload_from_filename(SS_FILEPATH)

        return jsonify(programs) if request else programs

    return 'Not Available!'


def programs_api(request):
    if request:
        fmt = request.args.get('format', 'json')
    else:
        fmt = None

    programs = _get_programs_from_cache()
    programs = _convert_dt(programs, to_str=False)

    if fmt == 'slack':
        formatted = _format_slack(programs)
    elif fmt == 'image':
        fp = _get_programs_ss_from_cache()
        return send_file(fp, mimetype='image/png')
    else:
        formatted = _convert_dt(programs, to_str=True)

    return jsonify(formatted) if request else formatted


if __name__ == "__main__":
    print(update_programs_cache(None))
    # print(programs_api(None))
