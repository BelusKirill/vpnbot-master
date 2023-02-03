from aiogram import Dispatcher
from datetime import datetime, timedelta
from loader import db, config

async def check_subscriptions(dp: Dispatcher):
    users = await db.get_access_for_check(datetime.now() - timedelta(days=2))
    for user in users:
        print(user['id_telegram'])
        try:
            if await check_subscriptions_shannel(dp.bot, user['id_telegram'], config.tg_bot.chanel_1, config.tg_bot.id_chanel_1):
                if await check_subscriptions_shannel(dp.bot, user['id_telegram'], config.tg_bot.chanel_2, config.tg_bot.id_chanel_2):
                    await db.set_access(user['id_telegram'], True)
                    return
            
            await db.set_access(user['id_telegram'], False)
        except Exception as ex:
            print('Ошибка', ex)
    pass

async def check_subscriptions_shannel(bot, id_user, chanel, id_chanel):
    cannal = f'@{chanel}' if id_chanel == '' else id_chanel
    user_channel_status = await bot.get_chat_member(chat_id=cannal, user_id=id_user)
    if user_channel_status["status"] != 'left':
        return True
    else:
        return False