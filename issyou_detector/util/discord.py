# encoding=utf-8
__all__ = (
    "to_stroke",
    "to_masked_link",
    "to_block_quote",
    "to_channel_mention",
)

def to_stroke(text: str) -> str:
    return "\n".join(
        f"~~{line.replace("~", "\\~")}~~"
        for line in text.splitlines()
    )

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
