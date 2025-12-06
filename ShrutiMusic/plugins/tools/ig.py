import re
import requests
from pyrogram import filters
from pyrogram.types import Message

from ShrutiMusic import app

# Regex to match Instagram URLs
INSTA_URL_REGEX = re.compile(r"^(https?://)?(www\.)?(instagram\.com|instagr\.am)/.*$")


async def _process_reel(message: Message, url: str):
    """Process the Instagram reel URL and send video."""
    
    if not re.match(INSTA_URL_REGEX, url):
        return await message.reply_text(
            "Tʜᴇ URL ɪs ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ Iɴsᴛᴀɢʀᴀᴍ ʟɪɴᴋ."
        )
    
    a = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")

    api_url = f"https://insta-dl.hazex.workers.dev/?url={url}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        result = response.json()

        if result.get("error"):
            raise Exception(result.get("message", "API Error"))

        data = result.get("result")
        if not data:
            raise Exception("No downloadable data found.")

    except Exception as e:
        try:
            await a.edit(f"Eʀʀᴏʀ : {e}")
        except:
            await message.reply_text(f"Eʀʀᴏʀ : {e}")
        return

    # Extract data
    video_url = data.get("url")
    if not video_url:
        try:
            return await a.edit("Nᴏ ᴠɪᴅᴇᴏ URL ғᴏᴜɴᴅ.")
        except:
            return await message.reply_text("Nᴏ ᴠɪᴅᴇᴏ URL ғᴏᴜɴᴅ.")

    duration = data.get("duration", "N/A")
    quality = data.get("quality", "N/A")
    type_ext = data.get("extension", "N/A")
    size = data.get("formattedSize", "N/A")

    caption = (
        f"Dᴜʀᴀᴛɪᴏɴ : {duration}\n"
        f"Qᴜᴀʟɪᴛʏ : {quality}\n"
        f"Tʏᴘᴇ : {type_ext}\n"
        f"Sɪᴢᴇ : {size}"
    )

    try:
        await message.reply_video(video_url, caption=caption)
        await a.delete()
    except Exception as e:
        await a.edit(f"Eʀʀᴏʀ ᴡʜɪʟᴇ sᴇɴᴅɪɴɢ ᴠɪᴅᴇᴏ: {e}")


@app.on_message(filters.command(["ig", "instagram", "reel"]))
async def download_instagram_command(client, message: Message):
    """Handles reel downloads via commands."""
    
    if len(message.command) < 2:
        return await message.reply_text(
            "Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ Iɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ URL."
        )

    url = message.text.split(None, 1)[1].strip()
    await _process_reel(message, url)


@app.on_message(
    filters.text
    & (filters.private | filters.group)
    & ~filters.via_bot
)
async def download_instagram_no_command(client, message: Message):
    """Handles reels when user sends only link."""
    
    if not message.text or message.text.startswith(('/', '!', '?', '.')):
        return

    url = message.text.strip()
    if re.match(INSTA_URL_REGEX, url):
        await _process_reel(message, url)


# Help Menu
MODULE = "Rᴇᴇʟ"
HELP = """
ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ:

• /ig [URL]
• /instagram [URL]
• /reel [URL]

Yᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴅᴏᴡɴʟᴏᴀᴅ ʀᴇᴇʟs ʙʏ sᴇɴᴅɪɴɢ ᴏɴʟʏ ᴛʜᴇ ʟɪɴᴋ.
"""
