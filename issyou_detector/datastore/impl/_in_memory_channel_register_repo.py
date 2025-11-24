# encoding=utf-8
__all__ = (
    "InMemoryChannelRegisterRepo",
)
import logging
import threading
from typing import override
from typing import Optional

from .._channel_register_repo import *
from ._simple_channel_register_repo import *

LOGGER = logging.getLogger(__name__)

class InMemoryChannelRegisterRepo(SimpleChannelRegisterRepo):
    def __init__(
        self,
    ):
        super().__init__()
        self.__guild_to_channels_map: SimpleChannelRegisterRepo._DATA_DICT = dict()

    @override
    async def _fetch_data(self) -> SimpleChannelRegisterRepo._DATA_DICT:
        return self.__guild_to_channels_map.copy()

    @override
    async def _save_data(self, data: SimpleChannelRegisterRepo._DATA_DICT) -> None:
        self.__guild_to_channels_map = data.copy()
