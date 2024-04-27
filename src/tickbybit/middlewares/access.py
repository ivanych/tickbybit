from typing import Any, Awaitable, Callable, Dict
import logging

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)


class AccessMiddleware(BaseMiddleware):
    """
    Мидлвер ограничивает доступ к боту. Доступ разрешается только для указанных пользователей.

    Любые обращения от всех прочих пользователей будут игнорироваться,
    при этом в лог будет записываться варнинг "Access denied for user (<данные пользователя>)".
    """

    def __init__(self, users: list[int]) -> None:
        """
        Мидлвер ограничивает доступ к боту. Доступ разрешается только для указанных пользователей.

        :param users: Список идентификаторов пользователей, которым разрешён доступ к боту
        """
        self.users = users

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if 'event_from_user' in data:
            user = data['event_from_user']

            if user.id in self.users:
                return await handler(event, data)

            logger.warning("Access denied for user (%s)", user)

        logger.warning('Access denied for unknown')
