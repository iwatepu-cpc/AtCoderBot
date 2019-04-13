#!/usr/bin/env python
# coding: utf-8
import schedule
from datetime import datetime
import time
import requests
import discord
import asyncio
import get_env
import contest_info as content

old_output = "【 開催予定コンテスト情報 】\n==================================\n開催予定情報なし\n==================================\n"
# old_output = ""
contestday_str = "**今日はコンテスト開催日！\nみんな頑張ろう！**\n.\n"

client = discord.Client()

# =====================================
# 定期実行関係 (webhookを使う)
# =====================================
def webhook(message):
   discord_webhook_url = get_env.WEBHOOK1
   data = {"content": " " + message + " "}
   requests.post(discord_webhook_url, data=data)

# 定期実行させたい処理
def regularly():
    global old_output

    print(datetime.now(), "更新チェック")
    content.scraping_info()
    now_output, is_today = content.get_upcoming()

    if old_output != now_output:
        old_output=now_output
        webhook(old_output)
    
    if is_today == True:
        webhook(contestday_str)

# 毎日12時30分
schedule.every().day.at("12:30").do(regularly)

@client.event
async def greeting_gm():
    while True:
        schedule.run_pending()
        await asyncio.sleep(3600)


# =====================================
# 返答型Bot関係
# =====================================
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    # channel_bot_test = [
    #     channel for channel in client.get_all_channels() if channel.name == 'general'][0]
    # await channel_bot_test.send(get_upcoming())
    await greeting_gm()

@client.event
async def on_message(message):
    # 「/readme」で始まるか調べる
    if message.content.startswith("/readme"):
        # 送り主がBotだった場合反応したくないので
        if client.user != message.author:
            # メッセージが送られてきたチャンネルへメッセージを送ります
            str = "**もう無能とは言わせない！！**\n" + \
                "あの **AtCoderBot** がまたまた帰ってきた！\n" + \
                "ユーザAPIに頼らず、独自にスクレイピングを行うように進化。\n" + \
                "定期的にコンテスト情報をチェックして、新着情報をお知らせするよ！\n" + \
                "`/コンテスト` でコンテストの開催予定を教えるよ！\n" + \
                "`/ENDコンテスト` で過去3回分の開催済みコンテストを教えるよ！\n" + \
                "この説明は `/readme` でいつでも聞けるよ！\n" + \
                "使いづらいクソBotだと感じた時は以下のリポジトリにプルリクしてね！" + \
                "https://github.com/iwatepu-cpc/AtCoderBot"
            await client.send_message(message.channel,str)

    # 「つかれた」で始まるか調べる
    if message.content.startswith("コンテストつかれた"):
        str = "コンテストお疲れ様！！\n" + \
            "レートは上がったかな？？ ^^"
        if client.user != message.author:
            await client.send_message(message.channel, str)

    # 「/コンテスト」で始まるか調べる
    if message.content.startswith("/コンテスト"):
        if client.user != message.author:
            output, is_today = content.get_upcoming()
            if is_today == True:
                await client.send_message(message.channel, contestday_str)
            await client.send_message(message.channel, output)


    # 「/ENDコンテスト」で始まるか調べる
    if message.content.startswith("/ENDコンテスト"):
        if client.user != message.author:
            await client.send_message(message.channel, content.get_recent()[0])

client.run(get_env.API_KEY)
