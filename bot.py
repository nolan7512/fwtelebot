# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 08:36:26 2023

@author: TuanKiet-Nguyen
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 16:22:14 2023

@author: TuanKiet-Nguyen
"""

import os
from telethon.sync import events,TelegramClient
from telethon import errors

# from telethon import TelegramClient

CHANNEL_USERNAMES = '1848177285,1923885339'
api_id = 26403417
api_hash = '33c9a5d269bc49c2dd7fbceda38b3a4f'
channel_usernames = CHANNEL_USERNAMES.split(',')
your_channel_username = '1940588455'
phone_number = '84973399573'
bot_api ='6386799203:AAF0FmGumSN40PsQfqEJ2rsHKk0dyAjQ4Oo'


try:
    print('Starting connect')
    client = TelegramClient(None, api_id, api_hash)
    print('Async  connect')
    client.connect()
except OSError:
    print('Failed to connect')



if not client.is_user_authorized():
    print("Kết nối fail.")
    # client.send_code_request(phone_number)
    # me = client.sign_in(phone_number, input('Enter code: '))
bot_active = True  # Biến để kiểm tra trạng thái hoạt động của bot

@client.on(events.NewMessage(chats=channel_usernames))
async def forward_message(event):
    if bot_active:
        original_message = event.message
        if original_message.reply_to_msg_id:
            # Nếu tin nhắn gốc là một reply
            original_reply_msg_id = original_message.reply_to_msg_id
            original_reply_message = await client.get_messages(event.chat_id, ids=original_reply_msg_id)
            new_message = await event.respond(original_message.text, reply_to=original_reply_message)
        else:
            new_message = await event.respond(original_message.text)
        await client.forward_messages(your_channel_username, new_message)

@client.on(events.NewMessage(pattern=r'^/start$'))
async def handle_start_command(event):
    global bot_active
    if not bot_active:
        bot_active = True
        await event.respond('Bot started.')
    else:
        await event.respond('Bot is already running.')

@client.on(events.NewMessage(pattern=r'^/stop$'))
async def handle_stop_command(event):
    global bot_active
    if bot_active:
        bot_active = False
        await event.respond('Bot stopped.')



try:
    client.start(bot_api)
except OSError:
    print('Failed bot_api to connect')

try:
    client.start()
except OSError:
    print('Failed start to connect')

client.run_until_disconnected()
