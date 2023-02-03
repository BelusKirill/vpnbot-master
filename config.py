from dataclasses import dataclass
from typing import List


@dataclass
class DbConfig:
    host: str
    port: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: List[int]
    ip: str
    port: int
    chanel_1: str
    chanel_2: str
    id_chanel_1: int
    id_chanel_2: int

@dataclass
class Webhook:
    url: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    webhook: Webhook


def load_config():
    from os import environ
    print(environ.get("BOT_TOKEN"))
    return Config(
        tg_bot=TgBot(
            token=environ.get("BOT_TOKEN"),
            admin_ids=list(map(int, environ.get("ADMIN").split(","))),
            ip=environ.get('BOT_IP'), port=int(environ.get("BOT_PORT")),
            chanel_1 = environ.get("CHANNEL_1"),
            chanel_2 = environ.get("CHANNEL_2"),
            id_chanel_1 = environ.get("ID_CHANNEL_1"),
            id_chanel_2 = environ.get("ID_CHANNEL_2")
        ),
        db=DbConfig(
            host=environ.get('DB_HOST'),
            password=environ.get('DB_PASS'),
            port=environ.get('DB_PORT'),
            user=environ.get('DB_USER'),
            database=environ.get('DB_NAME')
        ),
        webhook=Webhook(url=environ.get("SERVER_URL"))
    )
