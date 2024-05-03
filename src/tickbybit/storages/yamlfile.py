from typing import Any, Dict, Optional, cast
import logging

from aiogram.fsm.state import State
from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType

from tickbybit.settings import get_key, set_key, del_key

logger = logging.getLogger(__name__)


class FileStorage(BaseStorage):

    def __init__(self, file: str = '.settings/settings.yaml') -> None:
        """
        :param file: путь к yaml-файлу с контекстными данными.
        """
        self.file = file

    async def close(self) -> None:  # pragma: no cover
        """
        Close storage (database connection, file or etc.)
        """
        pass

    def _key(self, key: StorageKey) -> str:
        result_string = 'c' + str(key.chat_id) + '_u' + str(key.user_id)

        logger.info(f"_key: {result_string}")

        return result_string

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        """
        Set state for specified key

        :param key: storage key
        :param state: new state
        """
        state_key = self._key(key) + '_state'

        if state is None:
            del_key(file=self.file, path=state_key)
        else:
            set_key(
                file=self.file,
                path=state_key,
                value=cast(str, state.state if isinstance(state, State) else state),
            )

    async def get_state(self, key: StorageKey) -> Optional[str]:
        """
        Get key state

        :param key: storage key
        :return: current state
        """
        state_key = self._key(key) + '_state'

        value = get_key(file=self.file, path=state_key)

        return cast(Optional[str], value)

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        """
        Write data (replace)

        :param key: storage key
        :param data: new data
        """
        data_key = self._key(key) + '_data'

        if not data:
            del_key(file=self.file, path=data_key)
            return

        set_key(
            file=self.file,
            path=data_key,
            value=data,
        )

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        """
        Get current data for key

        :param key: storage key
        :return: current data
        """
        data_key = self._key(key) + '_data'

        value = get_key(file=self.file, path=data_key)

        if value is None:
            return {}

        return cast(Dict[str, Any], value)
