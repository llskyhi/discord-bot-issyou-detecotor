# encoding=utf-8
__all__ = (
    "ChannelRegisterRepo",
    "ChannelRegisterException",
    "ChannelAlreadyRegisteredError",
    "ChannelNotRegisteredError",
)
import abc
from typing import Optional

class ChannelRegisterRepo(abc.ABC):
    """
    Abstract base class for Issyou Detector data store repositories.
    """

    @abc.abstractmethod
    async def get_report_channel(
        self,
        guild_id: int,
        /,
    ) -> Optional[int]:
        """
        Get the channel to report detected messages in the given guild.

        Due to the fact that channel may have changed after once registered,
        caller has responsibility validating whether the returned channel ID is still valid.
        """

    @abc.abstractmethod
    async def register_report_channel(
        self,
        guild_id: int,
        channel_id: int,
        /,
    ) -> None:
        """
        Register a channel to report detected messages in the given guild.

        Raises:
            ChannelAlreadyRegisteredError: If there is already a channel registered.
        """

    @abc.abstractmethod
    async def unregister_report_channel(
        self,
        guild_id: int,
        /,
    ) -> int:
        """
        Unregister the channel from reporting detected messages in the given guild.

        Raises:
            ChannelNotRegisteredError: If there is no channel registered.

        Returns:
            The ID of the unregistered channel.
        """

class ChannelRegisterException(RuntimeError):
    """
    Base class for exceptions in the datastore module.
    """

class ChannelAlreadyRegisteredError(ChannelRegisterException):
    """
    Error that attempting to register a report channel in a guild
    while there is already a channel registered.
    """
    def __init__(
        self,
        guild_id: int,
        channel_id: int
    ):
        super().__init__()
        self.guild_id = guild_id
        self.channel_id = channel_id

class ChannelNotRegisteredError(ChannelRegisterException):
    """
    Error that attempting to unregister report channel in a guild
    while there is no channel registered.
    """
    def __init__(
        self,
        guild_id: int,
    ):
        super().__init__()
        self.guild_id = guild_id
