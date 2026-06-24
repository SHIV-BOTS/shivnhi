import math
import random
from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from PritiMusic import app
from PritiMusic.utils.formatters import time_to_seconds

# 🔥 PREMIUM EMOJIS
PREMIUM_EMOJIS = ["5422831825178206894", "5368324170673489600", "5206607081334906820", "5206380668048496464"]

def get_style_map():
    styles = [ButtonStyle.PRIMARY, ButtonStyle.SUCCESS, ButtonStyle.DANGER]
    random.shuffle(styles)
    return {1: styles[0], 2: styles[1], 3: styles[2], 4: styles[0]}

def create_btn(text, cb=None, url=None, style=ButtonStyle.PRIMARY):
    kwargs = {"text": text, "style": style}
    if cb: kwargs["callback_data"] = cb
    if url: kwargs["url"] = url
    return InlineKeyboardButton(**kwargs)

def clone_button(style):
    return create_btn("『 ✦ 𝐂ʟᴏηє 𝐌є ✦ 』", url="https://t.me/SizzuMusicBot", style=style)

def get_main_controls(chat_id, s_map):
    return [
        create_btn("▷", f"ADMIN Resume|{chat_id}", style=s_map[3], no_emoji=True),
        create_btn("II", f"ADMIN Pause|{chat_id}", style=s_map[3], no_emoji=True),
        create_btn("↻", f"ADMIN Replay|{chat_id}", style=s_map[3], no_emoji=True),
        create_btn("‣‣I", f"ADMIN Skip|{chat_id}", style=s_map[3], no_emoji=True),
        create_btn("▢", f"ADMIN Stop|{chat_id}", style=s_map[3], no_emoji=True),
    ]

def get_footer_row(chat_id, s_map):
    return [
        create_btn("❖ 𝐀ᴜᴛᴏ𝐏ʟᴀʏ ❖", f"ADMIN Autoplay|{chat_id}", style=s_map[1]),
        clone_button(s_map[1])
    ]

def stream_markup(chat_id):
    s = get_style_map()
    return InlineKeyboardMarkup([get_main_controls(chat_id, s), get_footer_row(chat_id, s)])

def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    filled = int((played_sec / duration_sec) * 10) if duration_sec != 0 else 0
    bar = "▰" * filled + "▱" * (10 - filled)
    s = get_style_map()
    return InlineKeyboardMarkup([[create_btn(f"{played} {bar} {dur}", cb="GetTimer", style=s[1], no_emoji=True)], 
                                 *stream_markup(chat_id).inline_keyboard])

def track_markup(_, videoid, user_id, channel, fplay):
    s = get_style_map()
    return InlineKeyboardMarkup([[create_btn(_["P_B_1"], f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}", s[2]),
                                 create_btn(_["P_B_2"], f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}", s[2])],
                                [clone_button(s[1])]])

def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    s = get_style_map()
    return InlineKeyboardMarkup([[create_btn(_["P_B_1"], f"LuckyPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}", s[2]),
                                 create_btn(_["P_B_2"], f"LuckyPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}", s[2])],
                                [clone_button(s[1])]])

def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    s = get_style_map()
    return InlineKeyboardMarkup([[create_btn(_["P_B_3"], f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}", s[1])],
                                [clone_button(s[1])]])

def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    s = get_style_map()
    return InlineKeyboardMarkup([[create_btn(_["P_B_1"], f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}", s[2]),
                                 create_btn(_["P_B_2"], f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}", s[2])],
                                [create_btn("◁", f"slider B|{query_type}|{query[:20]}|{user_id}|{channel}|{fplay}", s[3], True),
                                 create_btn("▷", f"slider F|{query_type}|{query[:20]}|{user_id}|{channel}|{fplay}", s[3], True)],
                                [clone_button(s[1])]])

def queue_markup(_, videoid, chat_id):
    s = get_style_map()
    return InlineKeyboardMarkup([[create_btn(_["S_B_3"], url=f"https://t.me/{app.username}?startgroup=true", style=s[1])],
                                *stream_markup(chat_id).inline_keyboard,
                                [create_btn("ᴍᴏʀᴇ", f"PanelMarkup None|{chat_id}", s[1])]])

def panel_markup_clone(_, vidid, chat_id, played, dur):
    s = get_style_map()
    return InlineKeyboardMarkup([[create_btn(f"{played} {dur}", "GetTimer", s[1], True)],
                                *stream_markup(chat_id).inline_keyboard,
                                [create_btn("<- 20s", f"ADMIN SeekBack|{chat_id}", s[4], True),
                                 create_btn("20s + ->", f"ADMIN SeekForward|{chat_id}", s[4], True)]])

def stream_markup2(_, chat_id): return stream_markup(chat_id)
def stream_markup_timer2(_, chat_id, played, dur): return stream_markup_timer(_, chat_id, played, dur)
def panel_markup_1(_, videoid, chat_id): return queue_markup(_, videoid, chat_id)
def panel_markup_2(_, videoid, chat_id): return queue_markup(_, videoid, chat_id)
def panel_markup_3(_, videoid, chat_id): return queue_markup(_, videoid, chat_id)
def panel_markup_5(_, videoid, chat_id): return queue_markup(_, videoid, chat_id)
def panel_markup_4(_, vidid, chat_id, played, dur): return panel_markup_clone(_, vidid, chat_id, played, dur)
    
