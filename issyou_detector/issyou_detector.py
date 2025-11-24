# encoding=utf-8
__all__ = (
    "IssyouDetector",
)

import logging
import os
from typing import Optional

import discord
import discord.ext.commands

from issyou_detector.cog import ChannelRegisterCog, VersionCog
from issyou_detector.datastore import ChannelRegisterRepo

LOGGER = logging.getLogger(__name__)

_MYGO_COLOR: int = 0x3388BB

class IssyouDetector(discord.ext.commands.Bot):
    """
    A Discord bot that detects messages containing "一生" or similar keywords,
    forward it to configured channel(s) so everyone can get notified.
    :D
    """
    def __init__(
        self,
        *,
        channel_register_repo: ChannelRegisterRepo,
    ):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix="/",
            intents=intents,
        )

        self._channel_register_repo = channel_register_repo

        LOGGER.info(f"Using ChannelRegisterRepo implementation: {channel_register_repo}.")

        self.__dev_guild: Optional[discord.abc.Snowflake] = None
        self.__dev_guild_initialized: bool = False

    async def on_ready(self):
        LOGGER.info(f"Successfully logged in as {self.user}.")
        LOGGER.debug(f"Bot user details: {self.user!r}.")

        LOGGER.info("Loading Cogs...")
        for cog in (
            VersionCog(),
            ChannelRegisterCog(
                channel_register_repo=self._channel_register_repo,
            ),
        ):
            await self.add_cog(cog)
        LOGGER.info("Cogs loaded.")

        if self._dev_guild is not None:
            # https://stackoverflow.com/questions/75136546/slash-commands-not-syncing-to-specific-guilds-in-discord-py
            self.tree.copy_global_to(guild=self._dev_guild)
        synced_commands = await self.tree.sync(guild=self._dev_guild)
        LOGGER.info(f"{len(synced_commands)} commands synced {"globally" if self._dev_guild is None else f"in dev guild {self._dev_guild.id}"}.")
        LOGGER.debug(f"Synced commands: {synced_commands}.")

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if message.guild is None:
            LOGGER.warning(f"Ignoring message outside guild (probably private message?).")
            return

        if not self._contains_issyou(message):
            LOGGER.debug(f"The message is considered not containing target content.")
            return

        LOGGER.info(f"Target content detected in guild {str(message.guild)!r}, channel {str(message.channel)!r}, by user {str(message.author)!r}.")
        LOGGER.debug(f"Detected message details: {message!r}.")
        await self._handle_target_message(message)

    @property
    def _dev_guild(self) -> Optional[discord.abc.Snowflake]:
        """
        Discord guild for development.
        """
        if self.__dev_guild_initialized:
            return self.__dev_guild

        LOGGER.debug("Checking dev guild configuration...")
        ENVIRONMENT_VARIABLE_NAME = "DEV_DISCORD_GUILD_ID"
        config_value = os.environ.get(ENVIRONMENT_VARIABLE_NAME)
        if config_value is None:
            self.__dev_guild = None
        else:
            try:
                guild_id = int(config_value)
            except ValueError as exception:
                LOGGER.warning(f"Failed to parse dev guild ID from environment variable {ENVIRONMENT_VARIABLE_NAME!r} with value {config_value!r}.", exc_info=exception)
                self.__dev_guild = None
            else:
                self.__dev_guild = discord.Object(id=guild_id)
                dev_guild = self.get_guild(guild_id)
                if dev_guild is None:
                    LOGGER.warning(f"Dev guild {guild_id!r} not found. Considering as not set.")
                    self.__dev_guild = None
                else:
                    self.__dev_guild = dev_guild
        LOGGER.debug(f"Using dev guild: {self.__dev_guild!r}.")
        self.__dev_guild_initialized = True
        return self.__dev_guild

    def _contains_issyou(self, message: discord.Message) -> bool:
        keywords = (
            "一輩子",
            "一生",
            "いっしょう",
        )
        if any(keyword in message.content.lower() for keyword in keywords):
            LOGGER.debug(f"Keyword found in `message.content` ({message.content!r}).")
            return True

        # TODO: embed content?

        return False

    async def _handle_target_message(self, message: discord.Message) -> None:
        report_channel = await self._get_report_channel(message)
        if report_channel is None:
            LOGGER.debug(f"No report channel available for guild {message.guild!r}. Aborting.")
            return
        LOGGER.debug(f"Forwarding message {message.id} to channel {report_channel!r}.")

        # TODO: additional reactions, like embed?
        # embed = self._build_notification_embed(message)
        await message.forward(report_channel)
        await report_channel.send(
            "いっしょう...！",
            # embed=embed,
        )

    async def _get_report_channel(
        self,
        message: discord.Message,
    ) -> Optional["discord.abc.MessageableChannel"]:
        guild: discord.Guild = message.guild
        report_channel_id = await self._channel_register_repo.get_report_channel(guild.id)
        if report_channel_id is None:
            LOGGER.info(f"No report channel configured in guild {message.guild}.")
            return None
        report_channel = guild.get_channel_or_thread(report_channel_id)
        if report_channel is None:
            LOGGER.warning(f"Report channel {report_channel_id!r} in guild {message.guild} is not found (may have been deleted?).")
            return None
        return report_channel

    def _build_notification_embed(
        self,
        message: discord.Message,
    ) -> discord.Embed:
        embed = discord.Embed(
            color=_MYGO_COLOR,
        )
        embed.set_author(
            name=message.author.display_name,
            icon_url=message.author.display_avatar.url,
        )
        return embed
