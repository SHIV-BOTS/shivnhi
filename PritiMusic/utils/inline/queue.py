import random
from typing import Union

from PritiMusic import app
from PritiMusic.utils.formatters import time_to_seconds
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# ✅ ButtonStyle Import for Kurigram Colors
from button import ButtonStyle

# ==========================================
# 🔥 PREMIUM EMOJIS & SMART BUTTON HELPER
# ==========================================
PREMIUM_EMOJIS = [
    "5422831825178206894", 
    "5368324170673489600",
    "5206607081334906820",
    "5206380668048496464"
]

def player_btn(text, callback_data=None, url=None, style=ButtonStyle.PRIMARY, use_emoji=False):
    """Helper function to create Kurigram formatted buttons safely."""
    kwargs = {"text": text, "style": style}
    if callback_data:
        kwargs["callback_data"] = callback_data
    if url:
        kwargs["url"] = url
    if use_emoji:
        kwargs["icon_custom_emoji_id"] = random.choice(PREMIUM_EMOJIS)
    return InlineKeyboardButton(**kwargs)

# ==========================================
# 🎵 QUEUE & STREAM MARKUPS
# ==========================================

def queue_markup(
    _,
    DURATION,
    CPLAY,
    videoid,
    played: Union[bool, int] = None,
    dur: Union[bool, int] = None,
):
    not_dur = [
        [
            player_btn(_["QU_B_1"], callback_data=f"GetQueued {CPLAY}|{videoid}", style=ButtonStyle.PRIMARY, use_emoji=True),
            player_btn(_["CLOSE_BUTTON"], callback_data="close", style=ButtonStyle.DANGER),
        ]
    ]
    dur_list = [
        [
            player_btn(_["QU_B_2"].format(played, dur), callback_data="GetTimer", style=ButtonStyle.SUCCESS)
        ],
        [
            player_btn(_["QU_B_1"], callback_data=f"GetQueued {CPLAY}|{videoid}", style=ButtonStyle.PRIMARY, use_emoji=True),
            player_btn(_["CLOSE_BUTTON"], callback_data="close", style=ButtonStyle.DANGER),
        ],
    ]
    upl = InlineKeyboardMarkup(not_dur if DURATION == "Unknown" else dur_list)
    return upl


def queue_back_markup(_, CPLAY):
    upl = InlineKeyboardMarkup(
        [
            [
                player_btn(_["BACK_BUTTON"], callback_data=f"queue_back_timer {CPLAY}", style=ButtonStyle.PRIMARY, use_emoji=True),
                player_btn(_["CLOSE_BUTTON"], callback_data="close", style=ButtonStyle.DANGER),
            ]
        ]
    )
    return upl


def aq_markup(_, chat_id):
    # Mini Player: Strict Color Coding
    buttons = [
        [
            player_btn("▷", callback_data=f"ADMIN Resume|{chat_id}", style=ButtonStyle.SUCCESS),
            player_btn("II", callback_data=f"ADMIN Pause|{chat_id}", style=ButtonStyle.SECONDARY),
            player_btn("↻", callback_data=f"ADMIN Replay|{chat_id}", style=ButtonStyle.PRIMARY),
            player_btn("‣‣I", callback_data=f"ADMIN Skip|{chat_id}", style=ButtonStyle.PRIMARY),
            player_btn("▢", callback_data=f"ADMIN Stop|{chat_id}", style=ButtonStyle.DANGER),
        ],
        [
            player_btn(_["CLOSE_BUTTON"], callback_data="close", style=ButtonStyle.DANGER),
        ],
    ]
    return buttons


def queuemarkup(_, vidid, chat_id):
    # Main Player: Strict Color Coding & Emojis on Prominent Links
    buttons = [
        [
            player_btn(_["S_B_5"], url=f"https://t.me/{app.username}?startgroup=true", style=ButtonStyle.PRIMARY, use_emoji=True),
        ],
        [
            player_btn("ᴘᴀᴜsᴇ", callback_data=f"ADMIN Pause|{chat_id}", style=ButtonStyle.SECONDARY),
            player_btn("sᴛᴏᴘ", callback_data=f"ADMIN Stop|{chat_id}", style=ButtonStyle.DANGER),
            player_btn("sᴋɪᴘ", callback_data=f"ADMIN Skip|{chat_id}", style=ButtonStyle.PRIMARY),
        ],
        [
            player_btn("ʀᴇsᴜᴍᴇ", callback_data=f"ADMIN Resume|{chat_id}", style=ButtonStyle.SUCCESS),
            player_btn("ʀᴇᴘʟᴀʏ", callback_data=f"ADMIN Replay|{chat_id}", style=ButtonStyle.PRIMARY),
        ],
        [
            player_btn("๏ ᴍᴏʀᴇ ๏", url="https://t.me/betabot_hub", style=ButtonStyle.PRIMARY, use_emoji=True),
        ],
    ]
    return buttons
