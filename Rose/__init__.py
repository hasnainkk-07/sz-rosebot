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
from config import *

UPDATES_CHANNEL = "https://t.me/Raiden_Support"
SUPPORT_GROUP = "https://t.me/Raiden_Updates"

SUDOERS = [1805959544, 5907205317, 1284920298, 5881613383]
LOG_GROUP_ID = -1002105665930
MOD_LOAD = []
MOD_NOLOAD = []
bot_start_time = time.time()

DB_URI = "RaidenRobot"
MONGO_URL = "mongodb+srv://herobh123456:hasnainkk07@hasnainkk07.uqjekii.mongodb.net/?retryWrites=true&w=majority"
OWNER_ID = 6346273488

myclient = pymongo.MongoClient(DB_URI)
dbn = myclient["Shikari"]

mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client.Shikari

app = Client("Shikari", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)
#    await app.start()



    # Initialize aiohttp session within an active event loop
aiohttpsession = ClientSession()

arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

    
bot = app
   
    x = await app.get_me()

    BOT_ID = int(BOT_TOKEN.split(":")[0])
    BOT_NAME = x.first_name + (x.last_name or "")
    BOT_USERNAME = x.username
    BOT_MENTION = x.mention
    BOT_DC_ID = x.dc_id

    print(f"BOT_NAME: {BOT_NAME}")
    print(f"BOT_USERNAME: @{BOT_USERNAME}")

    # Keep the application running
    await asyncio.Event().wait()


async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})


#*if __name__ == "__main__":
   # asyncio.run(main())
 
