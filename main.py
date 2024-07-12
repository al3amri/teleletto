import requests
from bs4 import BeautifulSoup
from datetime import datetime
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from flask import Flask
from keep_alive import keep_alive
keep_alive()

# Set up the Telegram bot
bot_token = '5692403421:AAGhk6IzZbo99myH6pIRrQajmnXZVTtqq1g'
DPurl = "postgresql://postgres:4hiHRQPx4HJgUv1LTKYk@containers-us-west-52.railway.app:7146/railway"
bot = telegram.Bot(token=bot_token)

# Define a command handler for the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to my TikTok info bot! Send me a TikTok username to get started.\n/info [USERNAME]")

# Define a command handler for the /info command
def info(update, context):
    # Get the username from the user's message
    username = context.args[0]

    # Get the user info from TikTok
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
    r = requests.get(f"https://www.tiktok.com/@{username}", headers=headers)
    server_log = str(r.text)

    soup = BeautifulSoup(server_log, 'html.parser')
    script = soup.find(id='SIGI_STATE').contents
    data = str(script).split('},"UserModule":{"users":{')[1]
    data_json = data
    userID = data.split('"id":"')[1].split('",')[0]
    name = data.split(',"nickname":"')[1].split('",')[0]
    secID = data.split(',"secUid":"')[1].split('"')[0]
    followers = data.split('"followerCount":')[1].split(',')[0]
    following = data.split('"followingCount":')[1].split(',')[0]
    likes = data.split('"heartCount":')[1].split(',')[0]
    videoCount = data.split('"videoCount":')[1].split(',')[0]
    signature = data.split('"signature":')[1].split(',')[0]
    region = data.split('"region":"')[1].split('"')[0]
    checkverified = data.split('"verified":')[1].split(',')[0]
    checkprivate = data.split('"privateAccount":')[1].split(',')[0]
    time = data.split('"nickNameModifyTime":')[1].split(',')[0]
    lastchangeuser = datetime.fromtimestamp(int(time))
    url_id = int(userID)

    binary = "{0:b}".format(url_id)
    i = 0
    bits = ""
    while i < 31:
        bits += binary[i]
        i += 1
    timestamp = int(bits, 2)
    dt_object = datetime.fromtimestamp(timestamp)

    # Send the user info to the user
  
    message = f"[ Get Info For @{username} ] ..\n"
    message += f"UserID : {userID}\n"
    message += f"Nickname : {name}\n"
    message += f"Bio : {signature}\n"
    message += f"Is Verified : {checkverified}\n"
    message += f"Is Private : {checkprivate}\n"

    message += f"Followers : {followers}\n"
    message += f"Following : {following}\n"
    message += f"Likes : {likes}\n"
    message += f"Total Videos : {videoCount}\n"
    message += f"User Create Time : {dt_object}\n"
    message += f"Last Time Change Nickname : {lastchangeuser}\n"
    message += f"Account Region : {region}\n\n"
    message += f"secUid : {secID}\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Set up the command handlers
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('info', info))

# Start the bot
updater.start_polling()
print("The bot is [ACTIVE]")
