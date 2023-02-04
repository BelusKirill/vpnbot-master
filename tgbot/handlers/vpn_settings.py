from typing import Dict

import aiohttp.client_exceptions
from aiogram import Dispatcher, types
from aiogram.types import Message, CallbackQuery, ChatType
from aiohttp import ClientConnectorError

from loader import db, bot, outline
from tgbot.keyboards.callback_data_factory import vpn_callback
from tgbot.keyboards.inline import keyboard_servers_list


async def vpn_handler(message: Message):
    await bot.send_message(message.from_user.id, f'Выберите страну сервера', reply_markup=await keyboard_servers_list('new_key'))


async def vpn_callback_handler(callback_query: CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, f'Выберите страну сервера',
                           reply_markup=await keyboard_servers_list('new_key'))


async def get_new_key(callback_query: CallbackQuery, callback_data: Dict[str, str]):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    try:
        if bool(await db.check_key(callback_query.from_user.id)):
            data = await outline.create_key(await db.get_server_key(int(callback_data['server'])))
            await db.set_key(callback_query.from_user.id, data["accessUrl"])
            await bot.send_message(callback_query.from_user.id,
                                'Вставьте вашу ссылку доступа в приложение Outline:\n '\
                                f'`{data["accessUrl"]}`', parse_mode=types.ParseMode.MARKDOWN)
            await callback_query.answer()
        else:
            key = await db.get_key(callback_query.from_user.id)            
            await bot.send_message(callback_query.from_user.id, 'Ключ уже сгенерирован\n ' \
                                                                f'`{key}`', parse_mode=types.ParseMode.MARKDOWN)
    except ClientConnectorError:
        await bot.send_message(callback_query.from_user.id,
                               f'Не удалось связаться с сервером для получения ключа, попробуйте через какое-то время')
    except aiohttp.client_exceptions:
        await bot.send_message(callback_query.from_user.id,
                               f'Не удалось связаться с сервером для получения ключа, попробуйте через какое-то время')


def register_vpn_handlers(dp: Dispatcher):
    dp.register_message_handler(vpn_handler, commands=["vpn"], chat_type=ChatType.PRIVATE, is_access=True)
    dp.register_callback_query_handler(vpn_callback_handler, vpn_callback.filter(action_type='vpn_settings'), chat_type=ChatType.PRIVATE, is_access=True)
    dp.register_callback_query_handler(get_new_key, vpn_callback.filter(action_type='new_key'), chat_type=ChatType.PRIVATE, is_access=True)