# encoding=utf-8
__all__ = (
    "TextFormat",
    "format_text",
    "to_italics",
    "to_bold",
    "to_underlined",
    "to_stroke",
    "to_masked_link",
    "to_block_quote",
    "to_channel_mention",
)

import enum

class TextFormat(enum.Flag):
    """
    https://support.discord.com/hc/en-us/articles/210298617-Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline
    """
    ITALICS = enum.auto()
    BOLD = enum.auto()
    UNDERLINE = enum.auto()
    STRIKETHROUGH = enum.auto()

def format_text(
    text: str,
    /,
    *,
    flags: TextFormat,
) -> str:
    return "\n".join(
        _format_line(line, flags=flags)
        for line in text.splitlines()
    )

def to_italics(text: str) -> str:
    return format_text(text, flags=TextFormat.ITALICS)

def to_bold(text: str) -> str:
    return format_text(text, flags=TextFormat.BOLD)

def to_underlined(text: str) -> str:
    return format_text(text, flags=TextFormat.UNDERLINE)

def to_stroke(text: str) -> str:
    return format_text(text, flags=TextFormat.STRIKETHROUGH)

def to_masked_link(text: str, url: str) -> str:
    # TODO: escape characters?
    return f"[{text}]({url})"

def to_block_quote(text: str) -> str:
    return "\n".join(
        f"> {line}"
        for line in text.splitlines()
    )

def to_channel_mention(channel_id: int) -> str:
    return f"<#{channel_id}>"

# TODO: tricky interaction between \ and `
def _format_line(
    line: str,
    /,
    *,
    flags: TextFormat,
) -> str:
    if TextFormat.ITALICS in flags or TextFormat.BOLD in flags:
        line = line.replace("*", "\\*")
    if TextFormat.UNDERLINE in flags:
        line = line.replace("_", "\\_")
    if TextFormat.STRIKETHROUGH in flags:
        line = line.replace("~", "\\~")

    if (TextFormat.ITALICS in flags):
        line = f"*{line}*"
    if (TextFormat.BOLD in flags):
        line = f"**{line}**"
    if (TextFormat.UNDERLINE in flags):
        line = f"__{line}__"
    if (TextFormat.STRIKETHROUGH in flags):
        line = f"~~{line}~~"

    return line
