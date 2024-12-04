import asyncio
import time
from inspect import getfullargspec
from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client
from pyrogram.types import Message
from Python_ARQ import ARQ
import pymongo
import os
from config import Config

# Configuration
UPDATES_CHANNEL = "https://t.me/Raiden_Support"
SUPPORT_GROUP = "https://t.me/Raiden_Updates"
API_HASH = Config.API_HASH
API_ID = Config.API_ID
ARQ_API_URL = Config.ARQ_API_URL
ARQ_API_KEY = Config.ARQ_API_KEY
SUDOERS = [1805959544, 5907205317, 1284920298, 5881613383]
LOG_GROUP_ID = -1002105665930
MOD_LOAD = []
MOD_NOLOAD = []
bot_start_time = time.time()
BOT_TOKEN = Config.BOT_TOKEN
DB_URI = Config.BASE_DB
MONGO_URL = "mongodb+srv://herobh123456:hasnainkk07@hasnainkk07.uqjekii.mongodb.net/?retryWrites=true&w=majority"
OWNER_ID = 6346273488

# MongoDB Clients
myclient = pymongo.MongoClient(DB_URI)
dbn = myclient["Shikari"]

mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client.Shikari

# Pyrogram Bot Client
app = Client("hasnainkk", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Hardcoded Bot Info
BOT_ID = 6342456315
BOT_NAME = "Rᴀɪᴅᴇɴ ⋊ Sʜᴏɢᴜɴ"
BOT_USERNAME = "Raiden_Robot"
BOT_MENTION = "[Rᴀɪᴅᴇɴ ⋊ Sʜᴏɢᴜɴ](https://t.me/Raiden_Robot)"
BOT_DC_ID = 1

bot = app

# Async Initialization Function
async def main():
    print("[INFO]: Starting bot...")

    # Start Pyrogram client
    await app.start()

    # Initialize aiohttp session inside the event loop
    global aiohttpsession
    aiohttpsession = ClientSession()

    # Initialize ARQ client
    print("[INFO]: Initializing ARQ client...")
    global arq
    arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

    print(f"[INFO]: {BOT_NAME} is online as @{BOT_USERNAME}")

    # Keep the bot running
    await asyncio.Event().wait()

# Helper Function: eor (Edit or Reply)
async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})

# Run the Bot
if __name__ == "__main__":
    asyncio.run(main())
    
