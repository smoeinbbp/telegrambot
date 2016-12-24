#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sqlite3
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from datetime import datetime
import logging

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Welcome to 'Zero to Hero' Bot. Our channel address: telegram.me/zerotoheroir")

def getCm(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Thanks. Our channel address telegram.me/zerotoheroir")
    userInfo = update.message.chat
    userMessage = update.message.text
    userId = userInfo['id']
    userName = userInfo['username']
    userFirstName = userInfo['first_name']
    userLastName = userInfo['last_name']
    cn = sqlite3.connect("botDb.sqlite")
    cn.execute("PRAGMA ENCODING = 'utf8';")
    cn.text_factory = str
    cn.execute("CREATE TABLE IF NOT EXISTS user_comment(u_id MEDIUMINT, u_name VARCHAR(100), u_first_name VARCHAR(100), u_last_name VARCHAR(100), u_comment TEXT, u_time DATETIME);")
    cn.execute("INSERT INTO user_comment VALUES (?, ?, ?, ?, ?, ?);", (userId, userName, userFirstName, userLastName, userMessage, datetime.now()))
    cn.commit()
    cn.close()

def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Unknown Command!")


updater = Updater(token='YOUR TOKEN')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler([Filters.text], getCm)
dispatcher.add_handler(echo_handler)

unknown_handler = MessageHandler([Filters.command], unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()
updater.stop()