import typing

from aiogram.dispatcher.filters import BoundFilter

from loader import db


class AccessFilter(BoundFilter):
    key = 'is_access'

    def __init__(self, is_access: typing.Optional[bool] = None):
        self.is_access = is_access

    async def check(self, obj):
        if self.is_access is None:
            return False
        return bool(await db.get_access(obj.from_user.id)) == self.is_access