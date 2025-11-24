# encoding=utf-8
__all__ = (
    "JsonChannelRegisterRepo",
)
import json
import logging
import pathlib
from typing import override

from .._channel_register_repo import *
from ._simple_channel_register_repo import *
from ._single_file_channel_register_repo import *

LOGGER = logging.getLogger(__name__)

class JsonChannelRegisterRepo(SingleFileChannelRegisterRepo):
    def __init__(
        self,
        data_root_path: pathlib.Path,
    ):
        super().__init__(data_root_path)

    @property
    @override
    def _data_file_name(self) -> str:
        return "report-channels.json"

    @override
    async def _fetch_data_from_file(self, data_file_path: pathlib.Path) -> SimpleChannelRegisterRepo._DATA_DICT:
        try:
            with data_file_path.open("r", encoding="utf-8") as file:
                json_object = json.load(file)
                return {
                    record["guild_id"]: record["channel_id"]
                    for record in json_object
                }
        except OSError as error:
            LOGGER.debug(f"Failed to read file {data_file_path.as_posix!r} ({error}), considering as no data.")
            return {}

    @override
    async def _save_data_to_file(self, data_file_path: pathlib.Path, data: SimpleChannelRegisterRepo._DATA_DICT) -> None:
        json_object = tuple(
            {
                "guild_id": guild_id,
                "channel_id": channel_id,
            }
            for guild_id, channel_id in data.items()
        )
        data_file_path.parent.mkdir(parents=True, exist_ok=True)
        with data_file_path.open("w", encoding="utf-8") as file:
            json.dump(
                json_object,
                file,
                indent=4,
            )
