import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.getenv("25848910"))
API_HASH = os.getenv("004f00cfcbe7bc10d16d864c6099f980")
BOT_TOKEN = os.getenv("8418981103:AAFzGFdbJEeU13kX3a4budOf8lMhE5fe_hY")

app = Client("file2video", api_id=25848910, api_hash=004f00cfcbe7bc10d16d864c6099f980, bot_token=8418981103:AAFzGFdbJEeU13kX3a4budOf8lMhE5fe_hY)

async def run_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    return await proc.communicate()

@app.on_message(filters.private & (filters.document | filters.video))
async def convert(_, message: Message):
    m = await message.reply_text("📥 Downloading…")
    file = await message.download()
    await m.edit("🎬 Converting…")
    out = "output.mp4"
    cmd = f'ffmpeg -y -i "{file}" -c:v libx264 -c:a aac -movflags +faststart "{out}"'
    await run_cmd(cmd)
    await m.edit("📤 Uploading…")
    await message.reply_video(out)
    await m.delete()
    os.remove(file)
    os.remove(out)

app.run()
