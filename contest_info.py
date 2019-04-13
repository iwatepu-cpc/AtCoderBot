#!/usr/bin/env python
# coding: utf-8
import re
from datetime import datetime
import json
import urllib.request
from bs4 import BeautifulSoup

url = 'https://atcoder.jp/contests/?lang=ja'
base_url = 'https://atcoder.jp/contests/'


def scraping_info():
    try:
        response = urllib.request.urlopen(url)
        html = response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print('HTTPError: ', e)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")

    contest_keys = ["permanent", "upcoming", "recent"]
    data_keys = ["start_ditetime", "title", "duration", "rated", "url"]
    contest_dict = {}

    for key, table in zip(contest_keys, soup.find_all("table", attrs={"class": "table"})):
        contests = []
        for tr in table.tbody.find_all('tr'):
            datas = [td.string for td in tr.find_all('td')]

            # permanentの例外処理
            if len(datas) < 4: datas = ["", datas[0], "", "-"]

            datas.append(tr.find(href=re.compile("/contests/")).get("href"))
            contests.append(dict(zip(data_keys, datas)))

        contest_dict[key] = contests

    fw = open("./contests.json", 'w', encoding='utf-8')
    json.dump(contest_dict, fw, indent=4, ensure_ascii=False)
    fw.close()


def get_info(table,max,output):
    is_today = False
    w_list = ['月', '火', '水', '木', '金', '土', '日']

    fw = open("./contests.json", 'r', encoding='utf-8')
    info_json = json.loads(fw.read())
    upcoming = info_json[table]

    for i, info in enumerate(upcoming):
        # 最新 max 件まで表示
        if i >= max: break

        # 開催日時取得
        start_ditetime = datetime.strptime(info["start_ditetime"], '%Y-%m-%d %H:%M:%S%z')
        start_dite = "{0:%Y/%m/%d}".format(start_ditetime.date())
        start_time = "{0:%H:%M}".format(start_ditetime.time())

        # コンテスト時間取得
        duration = info['duration']
        duration_min = list(map(int, duration.split(':')))
        duration_min = duration_min[0]*60+duration_min[1]

        block = "タイトル:" + info['title'] + "\n" + \
            "開催日　:" + start_dite + " (" + w_list[start_ditetime.weekday()] + ")\n" + \
            "開始時間:" + start_time + "～\n" + \
            "開催時間:" + duration + "(" + str(duration_min) + "分)\n" + \
            base_url + info['url'] + "\n" + \
            "==================================\n"

        if start_ditetime.date() == datetime.now().date():
            output += "***☆☆☆ 本日開催 ☆☆☆\n\n" + block + "***"
            is_today = True
        else:
            output += block
        
    return [output, is_today]

# =====================================
# 開催予定コンテスト取得
# =====================================
def get_upcoming():
    output = "【 開催予定コンテスト情報 (最新3つ)】\n" + \
        "==================================\n"
    return get_info("upcoming",3,output)


# =====================================
# 開催済みコンテスト出力
# =====================================
def get_recent():
    output = "【 開催済みコンテスト情報 (過去3回分)】\n" + \
        "==================================\n"
    return get_info("recent",3,output)


if __name__ == '__main__':
    scraping_info()

    out, is_today = get_upcoming()
    print(out)
    print("is_today=", is_today)

    out, is_today = get_recent()
    print(out)
    print("is_today=", is_today)
