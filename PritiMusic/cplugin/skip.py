import random
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message

import config
from PritiMusic import app
from PritiMusic.core.call import Lucky
from PritiMusic.misc import db

from PritiMusic.utils.database import get_loop
from PritiMusic.cplugin.utils.decorators.admins import AdminRightsCheck
from PritiMusic.utils.inline import close_markup
from PritiMusic.utils.stream.autoclear import auto_clean
from config import BANNED_USERS

@app.on_message(
    filters.command(["skip", "cskip", "next", "cnext"], prefixes=["/", "!", "%", ",", ".", "@", "#"])
    & filters.group 
    & ~BANNED_USERS
)
@AdminRightsCheck
async def skip(cli, message: Message, _, chat_id):
    # Queue check
    check = db.get(chat_id)
    if not check:
        return await message.reply_text(_["queue_2"])
        
    # Loop check
    loop = await get_loop(chat_id)
    if loop != 0:
        return await message.reply_text(_["admin_8"])

    # Multi-skip logic (e.g., /skip 3)
    skip_count = 1
    if len(message.command) > 1:
        state = message.text.split(None, 1)[1].strip()
        if state.isnumeric():
            state = int(state)
            if 1 <= state <= len(check):
                skip_count = state
            else:
                return await message.reply_text(_["admin_11"].format(len(check)))
        else:
            return await message.reply_text(_["admin_11"].format(len(check)-1))

    # 🟢 THE FIX: Synchronized Skip & Stream Change 🟢
    try:
        # Pehle (skip_count - 1) songs ko clean up karo
        if skip_count > 1:
            for x in range(skip_count - 1):
                try:
                    popped = check.pop(0)
                    if popped:
                        await auto_clean(popped)
                except:
                    pass
        
        # Sahi PyTgCalls client (assistant) nikalte hain clone ke liye
        pytgcalls_client = Lucky.one
        if chat_id in Lucky.active_clients and Lucky.active_clients[chat_id]:
            clients = Lucky.active_clients[chat_id]
            pytgcalls_client = clients[0] if isinstance(clients, list) else clients
                
        # Seedha change_stream call karo. 
        # Yeh automatic pop karega, next play karega, aur UI stream_card bhej dega!
        await Lucky.change_stream(pytgcalls_client, chat_id)
        
    except Exception as e:
        # Agar error aaya toh music stop karke bot bahar aa jayega gracefully
        try:
            await message.reply_text(
                text=_["admin_6"].format(message.from_user.mention, message.chat.title),
                reply_markup=close_markup(_)
            )
            await Lucky.stop_stream(chat_id)
        except:
            pass
