import asyncio
from inspect import getfullargspec
from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client
from pyrogram.types import Message
from Python_ARQ import ARQ
from config import Config
import pytz
from datetime import datetime

# Time and Date Setup
IST = pytz.timezone("Asia/Colombo")
current_time = datetime.now(IST)
date = current_time.strftime("%a/%d/%b/%Y %H:%M:%S")

# Configuration
MOD_LOAD = []
MOD_NOLOAD = []
LOG_GROUP_ID = Config.LOG_GROUP_ID
bot_start_time = current_time.timestamp()
MONGO_URL = Config.MONGO_URL
OWNER_ID = Config.OWNER_ID

# MongoDB Client
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client["supun"]

# Asynchronous Initialization
async def init():
    global aiohttpsession, arq, bot, app, BOT_ID, BOT_NAME, BOT_USERNAME, BOT_MENTION, BOT_DC_ID

    # Aiohttp Session
    try:
        aiohttpsession = ClientSession()
        print("Aiohttp session initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize Aiohttp session: {e}")
        return

    # ARQ Initialization
    try:
        arq = ARQ(Config.ARQ_API_URL, Config.ARQ_API_KEY, aiohttpsession)
        print("ARQ initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize ARQ: {e}")
        return

    # Pyrogram Clients
    bot = Client(
        "supun",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
    )
    app = Client(
        "app2",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID1,
        api_hash=Config.API_HASH1,
    )
    try:
        await bot.start()
        await app.start()
        print("Pyrogram clients started successfully.")
    except Exception as e:
        print(f"Failed to start Pyrogram clients: {e}")
        return

    # Fetch Bot Information
    x = await app.get_me()
    BOT_ID = x.id
    BOT_NAME = x.first_name + (x.last_name or "")
    BOT_USERNAME = x.username
    BOT_MENTION = x.mention
    BOT_DC_ID = x.dc_id

    print(f"Bot initialized: {BOT_NAME} (@{BOT_USERNAME})")

# Edit or Reply Helper Function
async def eor(msg: Message, **kwargs):
    func = (
        msg.edit_text
        if msg.from_user and msg.from_user.is_self
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})

# Cleanup on Exit
async def cleanup():
    try:
        await aiohttpsession.close()
        await bot.stop()
        await app.stop()
        print("Resources cleaned up successfully.")
    except Exception as e:
        print(f"Error during cleanup: {e}")

# Entry Point
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(init())
    except KeyboardInterrupt:
        print("Shutting down...")
        loop.run_until_complete(cleanup())
