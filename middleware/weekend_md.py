from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from datetime import datetime
from aiogram.types import Message


def _is_weekend() -> bool:
    return datetime.utcnow().weekday() in (5, 6)


class WeekendMessageMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:

        data['flag'] = True if _is_weekend() else False
        return await handler(event, data)
