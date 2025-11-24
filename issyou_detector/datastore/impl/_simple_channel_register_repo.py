# encoding=utf-8
__all__ = (
    "SimpleChannelRegisterRepo",
)
import abc
import logging
import threading
from typing import Optional, override

from .._channel_register_repo import *

LOGGER = logging.getLogger(__name__)

class SimpleChannelRegisterRepo(ChannelRegisterRepo):
    """
    Simple implement using an object representing all data,
    which the object is provided by subclasses.
    """
    _DATA_DICT = dict[int, int]
    """
    guild_id -> channel_id
    """

    def __init__(
        self,
    ):
        super().__init__()
        self.__datasource_lock = threading.RLock()

    @override
    async def get_report_channel(
        self,
        guild_id: int,
        /,
    ) -> Optional[int]:
        with self.__datasource_lock:
            guild_to_channels_map = await self._fetch_data()
            return guild_to_channels_map.get(guild_id, None)

    @override
    async def register_report_channel(
        self,
        guild_id: int,
        channel_id: int,
        /,
    ) -> None:
        with self.__datasource_lock:
            guild_to_channels_map = await self._fetch_data()
            registered_channel_id = guild_to_channels_map.get(guild_id, None)
            if registered_channel_id is not None:
                raise ChannelAlreadyRegisteredError(guild_id, registered_channel_id)
            LOGGER.debug(f"Registering report channel {channel_id!r} in guild {guild_id!r}.")
            guild_to_channels_map[guild_id] = channel_id
            await self._save_data(guild_to_channels_map)

    @override
    async def unregister_report_channel(
        self,
        guild_id: int,
        /,
    ) -> int:
        with self.__datasource_lock:
            guild_to_channels_map = await self._fetch_data()
            registered_channel_id = guild_to_channels_map.get(guild_id, None)
            if registered_channel_id is None:
                raise ChannelNotRegisteredError(guild_id)
            LOGGER.debug(f"Unregistering report channel {registered_channel_id!r} in guild {guild_id!r}.")
            del guild_to_channels_map[guild_id]
            await self._save_data(guild_to_channels_map)
            return registered_channel_id

    @abc.abstractmethod
    async def _fetch_data(self) -> _DATA_DICT:
        """
        Build the data object from the data source.
        """

    @abc.abstractmethod
    async def _save_data(self, data: _DATA_DICT) -> None:
        """
        Save the data object to the data source.
        """
