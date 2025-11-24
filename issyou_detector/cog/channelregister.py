# encoding=utf-8
__all__ = (
    "ChannelRegisterCog",
)
import logging

import discord.ext.commands
import discord.app_commands

from ..datastore._channel_register_repo import *
from ..util.discord import *

LOGGER = logging.getLogger(__name__)

class ChannelRegisterCog(discord.ext.commands.Cog):
    """
    Cog that defines commands for channel registration.
    """
    def __init__(
        self,
        *,
        channel_register_repo: ChannelRegisterRepo,
    ):
        super().__init__()
        self._channel_register_repo = channel_register_repo

    @discord.app_commands.command(
        name="show",
        description="確認目前這個伺服器中一輩子頻道🐧",
    )
    @discord.app_commands.guild_only
    async def _show_current_registered_channel(
        self,
        interaction: discord.Interaction,
    ) -> None:
        """
        Show registered channel in the guild.
        """
        guild: discord.Guild = interaction.guild
        LOGGER.info(f"User {interaction.user} is attempting to see registered channel within guild {guild!r}.")

        registered_channel_id = await self._channel_register_repo.get_report_channel(guild.id)

        if registered_channel_id is None:
            await interaction.response.send_message("目前沒有一輩子頻道🐧")
            return

        await interaction.response.send_message(f"目前的一輩子頻道：{to_channel_mention(registered_channel_id)}🐧")

    @discord.app_commands.command(
        name="test",
        description="測試一輩子警察能不能在一輩子頻道傳訊息🐧",
    )
    @discord.app_commands.guild_only
    async def _test_report_channel(
        self,
        interaction: discord.Interaction,
    ) -> None:
        """
        Test registered channel in the guild.
        """
        guild: discord.Guild = interaction.guild
        LOGGER.info(f"User {interaction.user} is testing registered channel within guild {guild!r}.")

        registered_channel_id = await self._channel_register_repo.get_report_channel(guild.id)

        if registered_channel_id is None:
            await interaction.response.send_message("目前沒有一輩子頻道🐧")
            return

        registered_channel = guild.get_channel_or_thread(registered_channel_id)
        if registered_channel is None:
            LOGGER.info(f"Testing registered channel failed: could not find the channel {registered_channel_id} in guild {guild!r}.")
            await interaction.response.send_message("測試失敗：找不到一輩子頻道")
            return
        if not isinstance(registered_channel, discord.abc.Messageable):
            LOGGER.warning(f"Testing registered channel failed: registered channel {registered_channel!r} in guild {guild!r} is not messageable.")
            await interaction.response.send_message(f"測試失敗：一輩子頻道{registered_channel.mention}無法傳送訊息")
            return
        try:
            test_message = await registered_channel.send(f"あっあー麥克風測試🐧")
        except discord.HTTPException as exception:
            LOGGER.info(f"Testing registered channel failed: could not send message to channel {registered_channel!r} in guild {guild!r}; reason: {exception.response.reason!r}.")
            LOGGER.debug("Exception info:", exc_info=exception)
            await interaction.response.send_message(f"測試一輩子頻道{registered_channel.mention}失敗🐧\n{to_block_quote(exception.text)}")
        else:
            await interaction.response.send_message(f"{to_masked_link("測試訊息", test_message.jump_url)}已傳送到{registered_channel.mention}🐧")
            # try to forward the message to validate the read message history permission
            response_message = await interaction.original_response()
            try:
                await response_message.forward(registered_channel)
            except discord.HTTPException as exception:
                LOGGER.exception(exception)
                await registered_channel.send(f"轉發測試失敗🐧\n{to_block_quote(exception.text)}")
            else:
                await registered_channel.send(f"轉發測試成功🐧")

    @discord.app_commands.command(
        name="issyou",
        description="在伺服器中的一個頻道訂下一輩子的約定🐧",
    )
    @discord.app_commands.guild_only
    async def _register_channel(
        self,
        interaction: discord.Interaction,
        text_channel: discord.TextChannel,
    ) -> None:
        """
        Register a channel to report detected messages.
        """
        guild: discord.Guild = interaction.guild
        LOGGER.info(f"User {interaction.user} is attempting to registering channel {text_channel.id!r} within guild {guild!r}.")

        registered_channel_info_message: str
        try:
            await self._channel_register_repo.register_report_channel(guild.id, text_channel.id)
        except ChannelAlreadyRegisteredError as exception:
            LOGGER.info(f"Guild {exception.guild_id!r} already has a registered report channel {exception.channel_id!r}. Overwriting it.")
            await self._channel_register_repo.unregister_report_channel(guild.id)
            await self._channel_register_repo.register_report_channel(guild.id, text_channel.id)
            registered_channel_info_message = f"{to_stroke(to_channel_mention(exception.channel_id))} {text_channel.mention}"
        else:
            registered_channel_info_message = text_channel.mention
        await interaction.response.send_message(f"{registered_channel_info_message} 🎵ずっと ずっと 離さないでいてー🎵")

    @discord.app_commands.command(
        name="kaisan",
        description="破棄這個伺服器中的一輩子約定🐧",
    )
    @discord.app_commands.guild_only
    async def _unregister_channel(
        self,
        interaction: discord.Interaction,
    ) -> None:
        """
        Unregister the channel in the guild from reporting detected messages.
        """
        guild: discord.Guild = interaction.guild
        LOGGER.info(f"User {interaction.user} is attempting to unregistering channel within guild {guild!r}.")

        try:
            unregistered_channel_id = await self._channel_register_repo.unregister_report_channel(guild.id)
        except ChannelNotRegisteredError as exception:
            LOGGER.info("Guild {interaction.guild_id!r} has no registered report channel to unregister.")
            await interaction.response.send_message("找不到...一輩子頻道在哪...")
        else:
            await interaction.response.send_message(f"{to_channel_mention(unregistered_channel_id)} 本当にやめちゃうの...？")
