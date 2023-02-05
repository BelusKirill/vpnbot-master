from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery, ChatType

from loader import bot, db, config
from tgbot.keyboards.inline import keyboard_start, keyboard_download, keyboard_channels


async def user_start(message: Message):
    await db.add_user(message.chat.id, message.chat.full_name)

    await message.answer('Приветствуем вас в одном из самых быстрых и безопасных VPN на основе протокола Shadowsocks!\n\n'
                         'С нашим VPN, вы забудете о расходе энергии, а приложения и социальные сети будут работать с высокой скоростью, без необходимости постоянно подключаться и отключаться.\n\n'
                         'Чтобы начать, скачайте приложение Outline по кнопке ниже.\n'
                         'После установки приложения, вернитесь в бота и нажмите кнопку «Подключиться». ',
                         reply_markup=keyboard_start(), disable_web_page_preview=True)

async def user_start_subscriptions(message: Message):
    await db.add_user(message.chat.id, message.chat.full_name)

    await message.answer('Для пользования функционалом бота, необходимо подписаться на каналы', reply_markup=keyboard_channels(), disable_web_page_preview=True)

async def check_subscriptions(callback_query: CallbackQuery):
    try:
        for i, channel in enumerate(config.tg_bot.channels):
            if await check_subscriptions_shannel(callback_query.message, callback_query.from_user.id, channel, config.tg_bot.id_channels[i]) == False:
                return

        await callback_query.message.delete()
        await db.set_access(callback_query.from_user.id, True)
        await user_start(callback_query.message)
    except Exception as ex:
        print('Ошибка', ex)

async def download_handler(message: Message):
    await message.answer(f'Приложение доступно для всех устройств!\n\n'
                         f'Лимит трафика ограничен до 250 гигабайт в месяц.\n\n'
                         f'Скачайте Outline и жмите кнопку Подключить, которая появляется в боте после оплаты подписки!\n\n'
                         f'Кнопка сама определит какая у вас операционная система и перенаправит вас в магазин для скачивания Outline.',
                         reply_markup=keyboard_download(), disable_web_page_preview=True)

async def help_handler(message: Message):
    await message.answer(f'На случай если у Вас возникли проблемы!\n\n'
                         f'1. Кнопка «Подключить» не срабатывает, что делать?\n'
                         f'Возможно вы не установили приложение Outline, скачайте и установите его сначала.\n\n'
                         f'2. Нажимаю кнопку «Подключить» в Outline, но он выдает ошибку, что делать?\n'
                         f'Закройте приложение Outline на 5-10 секунд и попробуйте подключиться снова.\n\n'
                         f'3. Есть ограничения по трафику в месяц?\n'
                         f'В месяц вы можете расходовать 250 гигабайт.\n\n'
                         f'4. Сколько устройств я могу подключить?\n'
                         f'Вы можете подключить неограниченное количество устройств с общим лимитом до 250 гигабайт в месяц.',
                        )


# ПЕРЕПИСАТЬ СООБЩЕНИЕ И ДОБАВИТЬ КНОПКУ в keyborads.inline
async def download_callback_handler(callback_query: CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id,
                           f'Приложение доступно для всех устройств!\n\n'
                           f'Лимит трафика ограничен до 250 гигабайт в месяц.\n\n'
                           f'Скачайте Outline и жмите кнопку Подключить, которая появляется в боте после оплаты подписки!\n\n'
                           f'Кнопка сама определит какая у вас операционная система и перенаправит вас в магазин для скачивания Outline.',
                           )

 # УБРАТЬ С КОМАНДЫ /HELP КНОПКИ
async def help_callback_handler(callback_query: CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id,
                           f'На случай если у Вас возникли проблемы!\n\n'
                           f'1. Кнопка «Подключить» не срабатывает, что делать?\n'
                           f'Возможно вы не установили приложение Outline, скачайте и установите его сначала.\n\n'
                           f'2. Нажимаю кнопку «Подключить» в Outline, но он выдает ошибку, что делать?\n'
                           f'Закройте приложение Outline на 5-10 секунд и попробуйте подключиться снова.\n\n'
                           f'3. Есть ограничения по трафику в месяц?\n'
                           f'В месяц вы можете расходовать 250 гигабайт.\n\n'
                           f'4. Сколько устройств я могу подключить?\n'
                           f'Вы можете подключить неограниченное количество устройств с общим лимитом до 250 гигабайт в месяц.',
                           reply_markup=None, disable_web_page_preview=True)

async def check_subscriptions_shannel(message: Message, id_user, chanel, id_chanel):
    cannal = f'@{chanel}' if id_chanel == 0 else id_chanel
    user_channel_status = await bot.get_chat_member(chat_id=cannal, user_id=id_user)
    if user_channel_status["status"] != 'left':
        return True
    else:
        await message.answer(f'Вы не подписанны на канал')
        return False


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], chat_type=ChatType.PRIVATE, is_access=True)
    dp.register_message_handler(download_handler, commands=["download"], chat_type=ChatType.PRIVATE, is_access=True)
    dp.register_callback_query_handler(download_callback_handler, lambda c: c.data == 'why', chat_type=ChatType.PRIVATE, is_access=True)
    dp.register_message_handler(help_handler, commands=["help"], chat_type=ChatType.PRIVATE, is_access=True)
    dp.register_callback_query_handler(help_callback_handler, lambda c: c.data == 'why', chat_type=ChatType.PRIVATE, is_access=True)

    dp.register_message_handler(user_start_subscriptions, chat_type=ChatType.PRIVATE, is_access=False)
    dp.register_callback_query_handler(check_subscriptions, lambda c: c.data == 'check_channels', chat_type=ChatType.PRIVATE, is_access=False)
