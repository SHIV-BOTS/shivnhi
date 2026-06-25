import os
from logging import getLogger
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from pyrogram import Client, filters, enums
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton

# 👇 Aapke PritiMusic repo se app import ho raha hai
from PritiMusic import app 

LOGGER = getLogger(__name__)

# --- Simple In-Memory Database ---
welcome_state = {}  # {chat_id: True/False}
last_welcome_msg = {}  # {chat_id: message_id}


# --- Image Processing Functions ---
def create_circular_pfp(pfp, size=(500, 500), brightness=1.3):
    # Image.ANTIALIAS is deprecated in new Pillow, use LANCZOS
    pfp = pfp.resize(size, Image.Resampling.LANCZOS).convert("RGBA")
    pfp = ImageEnhance.Brightness(pfp).enhance(brightness)
    
    # Create circular mask
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    
    pfp.putalpha(mask)
    return pfp

def generate_welcome_image(pic_path, user_id):
    # Apne repo me 'assets' folder banayein aur ye files wahan rakhein
    bg_path = "assets/wel2.png"
    font_path = "assets/font.ttf"
    
    background = Image.open(bg_path).convert("RGBA")
    
    try:
        pfp = Image.open(pic_path).convert("RGBA")
    except Exception:
        pfp = Image.open("assets/upic.png").convert("RGBA") # Default image
        
    pfp = create_circular_pfp(pfp)
    draw = ImageDraw.Draw(background)
    
    try:
        font = ImageFont.truetype(font_path, size=60)
    except Exception:
        font = ImageFont.load_default()
        
    # Text Draw Karna (Apne background ke hisab se coordinates adjust kar lein)
    draw.text((630, 450), f'ID: {user_id}', fill=(255, 255, 255), font=font)
    
    # Profile Pic paste karna
    background.paste(pfp, (48, 88), pfp)
    
    os.makedirs("downloads", exist_ok=True)
    output_path = f"downloads/welcome_{user_id}.png"
    background.save(output_path)
    return output_path


# --- Welcome Toggle Command ---
@app.on_message(filters.command("welcome") & filters.group)
async def toggle_welcome(client, message):
    user = await client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply("**sᴏʀʀʏ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴇɴᴀʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ!**")

    if len(message.command) != 2 or message.command[1].lower() not in ["on", "off"]:
        return await message.reply("**ᴜsᴀɢᴇ:**\n**⦿ /welcome [on|off]**")

    state = message.command[1].lower()
    chat_id = message.chat.id

    if state == "on":
        welcome_state[chat_id] = True
        await message.reply(f"**ᴇɴᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ɪɴ {message.chat.title}**")
    else:
        welcome_state[chat_id] = False
        await message.reply(f"**ᴅɪsᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ɪɴ {message.chat.title}**")


# --- Welcome Event Handler ---
@app.on_chat_member_updated(filters.group, group=-3)
async def greet_new_member(client, member: ChatMemberUpdated):
    chat_id = member.chat.id
    
    # Check if welcome is disabled (Default is ON)
    if welcome_state.get(chat_id, True) == False:
        return

    # Check if someone actually joined
    if not (member.new_chat_member and not member.old_chat_member and member.new_chat_member.status != enums.ChatMemberStatus.KICKED):
        return

    user = member.new_chat_member.user
    count = await client.get_chat_members_count(chat_id)

    # Old welcome message delete logic (spam rokne ke liye)
    if chat_id in last_welcome_msg:
        try:
            await last_welcome_msg[chat_id].delete()
        except Exception:
            pass

    try:
        # PFP Download
        try:
            pic_path = await client.download_media(user.photo.big_file_id, file_name=f"pp{user.id}.png")
        except AttributeError:
            pic_path = "assets/upic.png"

        welcome_img = generate_welcome_image(pic_path, user.id)
        
        bot_username = client.me.username if client.me else "my_bot"
        
        caption = f"""
**⎊─────☵ ᴡᴇʟᴄᴏᴍᴇ ☵─────⎊**

**▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬**

**☉ ɴᴀᴍᴇ ⧽** {user.mention}
**☉ ɪᴅ ⧽** `{user.id}`
**☉ ᴜ_ɴᴀᴍᴇ ⧽** @{user.username or "None"}
**☉ ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs ⧽** {count}

**▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬**

**⎉──────▢✭ 侖 ✭▢──────⎉**
"""
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("๏ ᴠɪᴇᴡ ɴᴇᴡ ᴍᴇᴍʙᴇʀ ๏", url=f"tg://openmessage?user_id={user.id}")],
            [InlineKeyboardButton("✙ ᴋɪᴅɴᴀᴘ ᴍᴇ ✙", url=f"https://t.me/{bot_username}?startgroup=true")],
        ])

        msg = await client.send_photo(chat_id, photo=welcome_img, caption=caption, reply_markup=markup)
        last_welcome_msg[chat_id] = msg
        
        # Cleanup: Generate hone ke baad files delete kar do taaki storage full na ho
        if os.path.exists(welcome_img):
            os.remove(welcome_img)
        if os.path.exists(pic_path) and pic_path != "assets/upic.png":
            os.remove(pic_path)

    except Exception as e:
        LOGGER.error(f"Welcome Error: {e}")
  
