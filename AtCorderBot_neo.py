#!/usr/bin/env python
# coding: utf-8
from datetime import datetime
import discord
import json
import urllib.request
import get_env


def getInfo(when):
    # API => https://github.com/kenkoooo/AtCoderProblems/

    url = 'https://kenkoooo.com/atcoder/resources/contests.json'
    base_url = 'https://atcoder.jp/contests/'
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

        output += "タイトル:" + info['title'] + "\n" + \
            "開催日　:" + "{0:%Y/%m/%d}".format(start_time.date()) + " (" + w_list[start_time.weekday()] + ")\n" + \
            "開催時間:" + "{0:%H:%M}".format(start_time.time()) + "～" + \
            "(" + str(duration) + "分)\n" + \
            base_url + info['id'] + "\n" + \
            "==================================\n"

    return output


client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    # channel_bot_test = [
    #     channel for channel in client.get_all_channels() if channel.name == 'general'][0]
    # await channel_bot_test.send(getInfo(1))


@client.event
async def on_message(message):
    # 「/readme」で始まるか調べる
    if message.content.startswith("/readme"):
        # 送り主がBotだった場合反応したくないので
        if client.user != message.author:
            # メッセージが送られてきたチャンネルへメッセージを送ります
            str = "あの **AtCorderBot** が帰ってきた！\n" + \
                "`/コンテスト` でコンテストの開催予定を教えるよ！\n" + \
                "`/ENDコンテスト` で過去3回分の開催済みコンテストを教えるよ！\n" + \
                "この説明は `/readme` でいつでも聞けるよ！\n" + \
                "使いづらいクソBotだと感じた時は以下のリポジトリにプルリクしてね！" + \
                "https://github.com/iwatepu-cpc/AtCorderBot"
            await client.send_message(message.channel,str)

    # 「/コンテスト」で始まるか調べる
    if message.content.startswith("/コンテスト"):
        if client.user != message.author:
            await client.send_message(message.channel, getInfo(1))

    # 「/ENDコンテスト」で始まるか調べる
    if message.content.startswith("/ENDコンテスト"):
        if client.user != message.author:
            await client.send_message(message.channel, getInfo(0))

client.run(get_env.API_KEY)
