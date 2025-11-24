# encoding=utf-8
__all__ = (
    "VersionCog",
)
import logging

import discord.ext.commands
import discord.app_commands

from .. import version as _version

LOGGER = logging.getLogger(__name__)

class VersionCog(discord.ext.commands.Cog):
    """
    Cog that defines commands for checking app version.
    """

    @discord.app_commands.command(
        name="version",
        description="確認一輩子警察的版本🐧",
    )
    @discord.app_commands.guild_only
    async def _show_current_version(
        self,
        interaction: discord.Interaction,
    ) -> None:
        """
        Show app version.
        """
        guild: discord.Guild = interaction.guild
        LOGGER.info(f"User {interaction.user} is attempting to see app version within guild {guild!r}.")

        await interaction.response.send_message(f"版本：{_version.__version__}")
