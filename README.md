# AtCorderBot

## AtCorderのコンテスト情報を教える Discord Bot です。 

AtCorderBot.py が2018年前期まで稼働していたコード。  
AtCorderBot_neo.py が現在運用しているコードです。  

## 動作環境
|               |            |
| :----------- | :-------- |
| Heroku        | (GitHub連携) |
| python        | 3.6.8      |
| discord.py    | 0.16.12    |
| python-dotenv | 0.10.1     |

## Heroku起動コマンド
```
heroku ps:scale bot=1
```