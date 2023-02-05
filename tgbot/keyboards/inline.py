import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import db, config
from .callback_data_factory import vpn_callback

logger = logging.getLogger(__name__)


def keyboard_start():
    keyboard = InlineKeyboardMarkup()
    inline_btn_1 = InlineKeyboardButton(f'1. Скачать приложение', url=f'https://dl.provpnbot.com/6gaa4')
    inline_btn_2 = InlineKeyboardButton(f'2. Подключиться', callback_data=vpn_callback.new(action_type='vpn_settings', server='no'))
    keyboard.row(inline_btn_1)
    keyboard.row(inline_btn_2)
    return keyboard

def keyboard_download():
    keyboard = InlineKeyboardMarkup()
    btn_download_client = InlineKeyboardButton(f'Установить приложение',
                                          url=f'https://dl.provpnbot.com/6gaa4')
    keyboard.row(btn_download_client)
    return keyboard

def keyboard_connect():
    keyboard = InlineKeyboardMarkup()
    btn_connect = InlineKeyboardButton(f'Подключиться',
                                          url=f'Здесь должна генерироваться ссылка')
    keyboard.row(btn_connect)
    return keyboard


async def keyboard_servers_list(action_type: str):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for x in await db.get_servers():
        keyboard.insert(InlineKeyboardButton(f'{x[0][1]}', callback_data=vpn_callback.new(action_type=action_type,
                                                                                          server=f'{x[0][0]}')))
    if action_type == 'to_delete':
        keyboard.row(InlineKeyboardButton(f'❌Выйти из меню', callback_data=f"cancel"))
    return keyboard


def keyboard_admin_action():
    keyboard = InlineKeyboardMarkup(row_width=2)
    btn_add_server = InlineKeyboardButton(f'Добавить сервер', callback_data='add_server')
    btn_delete_server = InlineKeyboardButton(f'Удалить сервер', callback_data='delete_server')
    btn_cancel = InlineKeyboardButton(f'❌Выйти из меню', callback_data=f"cancel")
    keyboard.add(btn_add_server, btn_delete_server, btn_cancel)
    return keyboard


def keyboard_cancel():
    return InlineKeyboardMarkup().add(InlineKeyboardButton(f'❌Выйти из меню', callback_data=f"cancel"))


def keyboard_channels():
    keyboard = InlineKeyboardMarkup(row_width=2)
    for i, channel in enumerate(config.tg_bot.channels):
        keyboard.add(InlineKeyboardButton(f'Канал {i+1}', url=f'https://t.me/{channel}'))
    check = InlineKeyboardButton(f'Проверить подписку', callback_data='check_channels')
    keyboard.add(check)
    return keyboard
