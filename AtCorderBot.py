#!/usr/bin/env python
# coding: utf-8
import datetime

import discord
import json
import urllib.request
import vcon
import get_env


def getInfo(when):
    # yk0nさんのAPI
    url = 'http://atcoder-api.yk0n.tk/api/v1/contests/upcoming_contest.json'
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
    }
    w_list = ['日', '月', '火', '水', '木', '金', '土']

    try:
        res = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(res)
        html = response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print('HTTPError: ', e)
    except json.JSONDecodeError as e:
        print('JSONDecodeError: ', e)

    if when == 1:
        output = "【 開催予定コンテスト情報 】\n" + \
                 "==================================\n"

        if len(json.loads(html)) <= 0:
            output += "開催予定情報なし\n" + \
                      "==================================\n"
            return output
    else:
        output = "【 開催済みコンテスト情報 】\n" + \
                 "==================================\n"

    for i, info in enumerate(json.loads(html)):
        if i == 3:
            break

        duration = int(info['duration'].split(":")[0]) * 60 + int(info['duration'].split(":")[1])
        date = info['date'].split(" ")[0].split("/")
        date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))

        if when == 1 and date.date() < datetime.date.today():
            break

        youbi = date.strftime('%w')

        output += "タイトル:" + info['name'] + "\n" + \
                  "開催日 :" + info['date'].split(" ")[0] + " (" + w_list[int(youbi)] + ")\n" + \
                  "開催時間:" + info['date'].split(" ")[1] + "～" + \
                  "(" + str(duration) + "分)\n" + \
                  info['url'] + "\n" + \
                  "==================================\n"

    # print(output)
    return output


client = discord.Client()


@client.event
async def on_ready():
    global flag
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    # 「コンテスト」で始まるか調べる
    if message.content.startswith("コンテスト"):
        # 送り主がBotだった場合反応したくないので
        if client.user != message.author:
            # メッセージを書きます
            m = getInfo(1)
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await client.send_message(message.channel, m)

    # 「過去のコンテスト」で始まるか調べる
    if message.content.startswith("過去のコンテスト"):
        # 送り主がBotだった場合反応したくないので
        if client.user != message.author:
            # メッセージを書きます
            m = getInfo(0)
            # メッセージが送られてきたチャンネルへメッセージを送ります
            await client.send_message(message.channel, m)

    if message.content.startswith('デュエルスタンバイ'):
        today = datetime.date.today()
        vcon.login('iwatepu_cpc', 'iwate-pu2')
        id = vcon.create_contest('岩手県立大学 競技プログラミングサークル#' + today.strftime("%Y/%m/%d"))
        args = message.content.split()
        if len(args) == 2:
            vcon.add_problem(id, args[1])
        else:
            vcon.add_problem(id, 'ABCD')
        await client.send_message(message.channel, "今日のVコンです。競技時間は21:00〜22:40で,ペナルティ5分です。\n" + vcon.get_contest_url(id))


client.run(get_env.API_KEY)

if __name__ == '__main__':
    print(getInfo())
