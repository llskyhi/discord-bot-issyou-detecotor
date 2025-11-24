# encoding=utf-8
__all__ = (
    "SingleFileChannelRegisterRepo",
)
import abc
import pathlib
from typing import Optional, override

from .._channel_register_repo import *
from ._simple_channel_register_repo import *

class SingleFileChannelRegisterRepo(SimpleChannelRegisterRepo):
    """
    guild_id -> channel_id
    """

    def __init__(
        self,
        data_root_path: pathlib.Path,
    ):
        super().__init__()
        self.__data_root_path = data_root_path

    def __str__(self):
        return f"{self.__class__.__name__}<data file path: {self.__data_file_path}>"

    @property
    @abc.abstractmethod
    def _data_file_name(self) -> str:
        """
        Get the data file name.
        """

    @override
    async def _fetch_data(self) -> SimpleChannelRegisterRepo._DATA_DICT:
        return await self._fetch_data_from_file(self.__data_file_path)

    @override
    async def _save_data(self, data: SimpleChannelRegisterRepo._DATA_DICT) -> None:
        await self._save_data_to_file(self.__data_file_path, data)

    @abc.abstractmethod
    async def _fetch_data_from_file(self, data_file_path: pathlib.Path) -> SimpleChannelRegisterRepo._DATA_DICT:
        pass

    @abc.abstractmethod
    async def _save_data_to_file(self, data_file_path: pathlib.Path, data: SimpleChannelRegisterRepo._DATA_DICT) -> None:
        pass

    @property
    def __data_file_path(self) -> pathlib.Path:
        return self.__data_root_path.joinpath(self._data_file_name)
