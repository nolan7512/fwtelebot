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
from telethon.sync import events
from telethon import TelegramClient

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
channel_usernames = os.environ.get('CHANNEL_USERNAMES').split(',')
your_channel_username = os.environ.get('YOUR_CHANNEL_USERNAME')
phone_number = os.environ.get('PHONE')

client = TelegramClient('autoforwardbotnolan', api_id, api_hash)
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone_number)
    me = client.sign_in(phone_number, input('Enter code: '))
bot_active = False  # Biến để kiểm tra trạng thái hoạt động của bot

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

client.start()
client.run_until_disconnected()
