# AtCoderBot

## AtCoderのコンテスト情報を教える Discord Bot です。 

AtCoderBot.py が2018年前期まで稼働していたコード。  
AtCoderBot_neo.py が現在運用しているコードです。  

## 動作環境
|               |            |
| :----------- | :-------- |
| Heroku        | (GitHub連携) |
| python        | 3.6.8      |
| discord.py    | 0.16.12    |
| python-dotenv | 0.10.1     |
| requests      | 2.21.0     |
| schedule      | 0.6.0      |

## Heroku起動コマンド
```
heroku ps:scale bot=1
```