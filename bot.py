import logging

from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()


def register_all_filters(dispatcher):
    from tgbot.filters.admin import AdminFilter
    from tgbot.filters.access import AccessFilter
    dispatcher.filters_factory.bind(AccessFilter)
    dispatcher.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    from tgbot.handlers.admin import register_admin
    from tgbot.handlers.cancel import register_cancel
    from tgbot.handlers.error_handler import register_error_handler
    from tgbot.handlers.user import register_user
    from tgbot.handlers.vpn_settings import register_vpn_handlers

    register_cancel(dp)
    register_admin(dp)
    register_user(dp)
    register_vpn_handlers(dp)
    register_error_handler(dp)

def scheduler_jods():
    from tgbot.handlers.schedul import check_subscriptions
    
    scheduler.add_job(check_subscriptions, "cron", hour=12, minute=00, args=(dp,))
    #scheduler.add_job(check_subscriptions, "interval", seconds=10, args=(dp,)) #test

async def on_startup(dispatcher):
    scheduler_jods()

    logging.basicConfig(
        level=logging.DEBUG,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    from loader import db
    if await db.create_pool():
        await db.create_servers_table()
        await db.create_users_table()
        register_all_filters(dispatcher)
        register_all_handlers(dispatcher)
        # If you use polling
        await dispatcher.bot.set_my_commands([
            BotCommand('start', 'Перезапустить 🔄'),
            BotCommand('vpn', 'Получить VPN 🛡'),
            BotCommand('download', 'Скачать приложение 📲'),
            BotCommand('help', 'Помощь 📖')
        ])

        # If you use webhook
        # Make sure you have opened the ports in docker-compose
        # await bot.set_webhook(f"{PATH}")


async def on_shutdown(dispatcher):
    from loader import db, outline
    logging.warning('Shutting down..')
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

    logging.warning('Bye!')
    await dispatcher.bot.close()
    await db.close()
    await outline.close()


if __name__ == '__main__':
    from aiogram.utils import executor
    from loader import dp #, config

    # If you use polling
    scheduler.start()
    executor.start_polling(dp, skip_updates=True,
                           on_startup=on_startup, on_shutdown=on_shutdown)
    # If you want to use webhooks.
    # Make sure you have opened the ports in docker-compose
    # executor.start_webhook(dispatcher=dp, webhook_path=f'{config.webhook.url}',
    #                        on_startup=on_startup, on_shutdown=on_shutdown,
    #                        skip_updates=True, host=f'{config.tg_bot.ip}', port=config.tg_bot.port)
