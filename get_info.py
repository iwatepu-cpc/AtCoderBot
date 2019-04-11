#!/usr/bin/env python
# coding: utf-8
from datetime import datetime
import json
import urllib.request

# API => https://github.com/kenkoooo/AtCoderProblems/
url = 'https://kenkoooo.com/atcoder/resources/contests.json'
base_url = 'https://atcoder.jp/contests/'


def get_info(when):
    is_today = False
    w_list = ['月', '火', '水', '木', '金', '土', '日']

    try:
        response = urllib.request.urlopen(url)
        html = response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print('HTTPError: ', e)

    info_json = json.loads(html)
    info_json.sort(key=lambda x: x['start_epoch_second'])
    info_json.reverse()

    if when == 0:
        output = "【 開催済みコンテスト情報 (過去3回分)】\n" + \
                 "==================================\n"
    else:
        output = "【 開催予定コンテスト情報 】\n" + \
            "==================================\n"

    for i, info in enumerate(info_json):
        start_time = info['start_epoch_second']
        start_time = datetime.fromtimestamp(start_time)

        if when == 0 and i == 3:
            break

        elif when == 1 and start_time < datetime.now():
            if i == 0:
                output += "開催予定情報なし\n" + \
                    "==================================\n"
            break

        duration = int(info['duration_second']/60)
        # print(start_time, w_list[start_time.weekday()],
        #       duration, info['rate_change'], info['title'])

        block = "タイトル:" + info['title'] + "\n" + \
            "開催日　:" + "{0:%Y/%m/%d}".format(start_time.date()) + " (" + w_list[start_time.weekday()] + ")\n" + \
            "開催時間:" + "{0:%H:%M}".format(start_time.time()) + "～" + \
            "(" + str(duration) + "分)\n" + \
            base_url + info['id'] + "\n" + \
            "==================================\n"

        if start_time.date() == datetime.now().date():
            output += "***☆☆☆ 本日開催 ☆☆☆\n\n" + block + "***"
            is_today = True
        else:
            output += block

    return [output, is_today]


if __name__ == '__main__':
    url = "file:./test.json"
    out, is_today = get_info(1)
    print(out)
    print("is_today=", is_today)
