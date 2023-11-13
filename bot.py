# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 13:43:46 2023

@author: TuanKiet-Nguyen
"""



import os
from telethon.sync import events,errors,TelegramClient
from telethon.sessions import StringSession


# from telethon import TelegramClient
api_id = int(os.environ.get("API_ID", 0))
api_hash = os.environ.get('API_HASH')
channel_usernames = os.environ.get('CHANNEL_USERNAMES','').split(',')
your_channel_username = os.environ.get('YOUR_CHANNEL_USERNAME')
phone_number = int(os.environ.get("PHONE_NUMBER", 0))
pass_code = int(os.environ.get("PASS_CODE", 0))
bot_token = os.environ.get('BOT_TOKEN')
#session_path = '/etc/secrets/bot_session_online.session'
session_path = os.environ.get('SESSION')
session_paths ='./bot_session_online.session'
 # Danh sách các từ cần lọc
filter_words = ['AUDCAD', 'AUDCHF', 'AUDJPY', 'AUDNZD', 'AUDUSD', 'CADCHF', 'CADJPY', 'CHFJPY', 'EURAUD', 'EURCAD', 'EURCHF', 'EURGBP', 'EURJPY', 'EURNZD', 'EURUSD', 'GBPAUD', 'GBPCAD', 'GBPCHF', 'GBPJPY', 'GBPNZD', 'GBPUSD', 'NZDCAD', 'NZDCHF', 'NZDJPY', 'NZDUSD', 'USDCAD', 'USDCHF', 'USDJPY', 'XAGUSD', 'XAUUSD','GOLD','AUD/CAD', 'AUD/CHF', 'AUD/JPY', 'AUD/NZD', 'AUD/USD', 'CAD/CHF', 'CAD/JPY', 'CHF/JPY', 'EUR/AUD', 'EUR/CAD', 'EUR/CHF', 'EUR/GBP', 'EUR/JPY', 'EUR/NZD', 'EUR/USD', 'GBP/AUD', 'GBP/CAD', 'GBP/CHF', 'GBP/JPY', 'GBP/NZD', 'GBP/USD', 'NZD/CAD', 'NZD/CHF', 'NZD/JPY', 'NZD/USD', 'USD/CAD', 'USD/CHF', 'USD/JPY', 'XAG/USD', 'XAU/USD']
filter_mode = True  # Trạng thái chế độ lọc
bot_active = True  # Biến để kiểm tra trạng thái hoạt động của bot
status_message = "Bot Started, Filter mode: ON"


try:
    print('Starting connect')
    client = TelegramClient(StringSession(session_path), api_id, api_hash)
    client.start(phone=phone_number, password=pass_code)
    client.send_message(your_channel_username, "Bot đã chạy thành công!")
    #client.start(bot_token=bot_token)
    #client.connect()
except OSError:
    print('Failed to connect')

@client.on(events.NewMessage(chats=channel_usernames))
async def forward_message(event):
    try:
        if bot_active:
            message_text = event.message.text.lower()  # Chuyển nội dung tin nhắn thành chữ thường
            if not filter_mode or any(word.lower() in message_text for word in filter_words):
                await client.send_message(your_channel_username, event.message.text)
    except Exception as e:
        print(f"Error in forward_message: {e}")

@client.on(events.NewMessage(pattern=r'^/startfw$'))
async def handle_start_command(event):
    global bot_active, status_message
    if not bot_active:
        bot_active = True
        filter_status = "ON" if filter_mode else "OFF"
        status_message = f"Bot started, Filter mode: {filter_status}"
        await event.respond(status_message)
    else:
        stratingtrue = "Bot already running"
        await event.respond(stratingtrue)

@client.on(events.NewMessage(pattern=r'^/stopfw$'))
async def handle_stop_command(event):
    global bot_active, status_message
    if bot_active:
        bot_active = False
        filter_status = "ON" if filter_mode else "OFF"
        status_message = f"Bot stopped, Filter mode: {filter_status}"
        await event.respond(status_message)
    else:
        stratingtrue = "Bot already Stop"
        await event.respond(stratingtrue)
   

@client.on(events.NewMessage(pattern=r'^/helpfw$'))
async def handle_help_command(event):    
    help_message = "Hướng dẫn sử dụng Bot Forward:\n\n"
    help_message += "/startfw: Bắt đầu hoạt động của bot.\n"
    help_message += "/stopfw: Dừng hoạt động của bot.\n"
    help_message += "/helpfw: Hiển thị hướng dẫn này.\n"
    help_message += "/filteron: Bật chế độ lọc từ trong tin nhắn.\n"
    help_message += "/filteroff: Tắt chế độ lọc từ trong tin nhắn.\n"
    help_message += "/statusfw: Hiển thị trạng thái của bot và chế độ lọc từ.\n"
    help_message += "/listchannel: Liệt kê danh sách các kênh hiện tại.\n"
    await event.respond(help_message)

@client.on(events.NewMessage(pattern=r'^/filteron$'))
async def handle_filteron_command(event):
    global filter_mode, status_message
    filter_mode = True
    status_message = "Bot started, Filter mode: ON"
    await event.respond(status_message)

@client.on(events.NewMessage(pattern=r'^/filteroff$'))
async def handle_filteroff_command(event):
    global filter_mode, status_message
    filter_mode = False
    status_message = "Bot started, Filter mode: OFF"
    await event.respond(status_message)

@client.on(events.NewMessage(pattern=r'^/statusfw$'))
async def handle_status_command(event):
    await event.respond(status_message)


@client.on(events.NewMessage(pattern=r'^/listchannel'))
async def handle_list_channel_command(event):
    channel_list = ', '.join(channel_usernames)
    await event.respond(f"Danh sách các kênh hiện tại: {channel_list}")

client.run_until_disconnected()
