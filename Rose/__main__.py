import asyncio
import importlib
import re
from contextlib import closing, suppress

from uvloop import install
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from Rose import app, bot, BOT_NAME, BOT_USERNAME
from Rose.plugins import ALL_MODULES
from Rose.utils import paginate_modules
from Rose.utils.start import get_private_rules, get_learn
from Rose.mongo.usersdb import adds_served_user, add_served_user
from Rose.mongo.chatsdb import add_served_chat
from Rose.plugins.fsub import ForceSub
from config import var
from lang import get_command
from Rose.utils.lang import language, languageCB

loop = asyncio.get_event_loop()
flood = {}
HELPABLE = {}

async def start_bot():
    global HELPABLE

    # Import all modules dynamically
    for module in ALL_MODULES:
        imported_module = importlib.import_module(f"Rose.plugins.{module}")
        if hasattr(imported_module, "__MODULE__") and hasattr(imported_module, "__HELP__"):
            HELPABLE[module.replace(" ", "_").lower()] = imported_module

    # Log imported modules
    all_modules = "\n".join([f"• Successfully imported: {module}.py" for module in ALL_MODULES])
    print(all_modules)
    print("""
    _____________________________________________
    |                                             |
    |          Deployed Successfully              |
    |         (C) 2021-2022 by @szteambots        |
    |          Greetings from Supun :)           |
    |_____________________________________________|
    """)

    await idle()
    await aiohttpsession.close()
    print("Stopping clients")
    await app.stop()
    print("Cancelling asyncio tasks")
    for task in asyncio.all_tasks():
        task.cancel()
    print("Bot offline")


@app.on_message(filters.command("start"))
@language
async def start(client, message: Message, _):
    chat_id = message.chat.id
    FSub = await ForceSub(bot, message)
    if FSub == 400:
        return
    if message.chat.type != "private":
        await message.reply_text(var.group_start_text)
        await adds_served_user(message.from_user.id)
        return await add_served_chat(chat_id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1].lower()
        if name.startswith("rules"):
            return await get_private_rules(app, message, name)
        if name.startswith("learn"):
            return await get_learn(app, message, name)
        if "_" in name:
            module = name.split("_", 1)[1]
            text = _["main6"].format(HELPABLE[module].__MODULE__) + HELPABLE[module].__HELP__
            await message.reply_text(text, disable_web_page_preview=True)
        if name == "help":
            text, keyb = await help_parser(message.from_user.first_name)
            await message.reply_text(_["main5"], reply_markup=keyb, disable_web_page_preview=True)
        if name == "connections":
            await message.reply(var.Connection_text_start)
    else:
        user_mention = message.from_user.mention
        await message.reply_text(
            var.pm_start_text.format(user_mention, BOT_NAME),
            reply_markup=var.home_keyboard_pm
        )
        return await add_served_user(chat_id)


@app.on_callback_query(filters.regex("_langs"))
@languageCB
async def commands_callback(client, CallbackQuery, _):
    await CallbackQuery.message.edit(
        text=var.lang_text,
        reply_markup=var.lang_keyboard,
        disable_web_page_preview=True
    )


@app.on_callback_query(filters.regex("_about"))
@languageCB
async def about_callback(client, CallbackQuery, _):
    await CallbackQuery.message.edit(
        text=_["menu"],
        reply_markup=var.about_buttons,
        disable_web_page_preview=True
    )


@app.on_message(filters.command("help"))
@language
async def help_command(client, message: Message, _):
    if message.chat.type != "private":
        if len(message.command) >= 2:
            name = message.text.split(None, 1)[1].replace(" ", "_").lower()
            if name in HELPABLE:
                help_keyboard_button = InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text=_["main3"], url=f"t.me/{BOT_USERNAME}?start=help_{name}")]]
                )
                await message.reply_text(_["main4"], reply_markup=help_keyboard_button)
            else:
                await message.reply_text(_["main2"])
        else:
            await message.reply_text(_["main2"])
    else:
        if len(message.command) >= 2:
            name = message.text.split(None, 1)[1].replace(" ", "_").lower()
            if name in HELPABLE:
                text = _["main6"].format(HELPABLE[name].__MODULE__) + HELPABLE[name].__HELP__
                button = HELPABLE[name].__helpbtns__ if hasattr(HELPABLE[name], "__helpbtns__") else []
                button += [[InlineKeyboardButton("« Back", callback_data="bot_commands")]]
                await message.reply_text(
                    text,
                    reply_markup=InlineKeyboardMarkup(button),
                    disable_web_page_preview=True
                )
            else:
                text, help_keyboard = await help_parser(message.from_user.first_name)
                await message.reply_text(
                    _["main5"],
                    reply_markup=help_keyboard,
                    disable_web_page_preview=True
                )
        else:
            text, help_keyboard = await help_parser(message.from_user.first_name)
            await message.reply_text(
                text, reply_markup=help_keyboard, disable_web_page_preview=True
            )


@app.on_callback_query(filters.regex("startcq"))
@languageCB
async def start_callback(client, CallbackQuery, _):
    user_mention = CallbackQuery.from_user.mention
    await CallbackQuery.message.edit(
        text=var.pm_start_text.format(user_mention, BOT_NAME),
        disable_web_page_preview=True,
        reply_markup=var.home_keyboard_pm
    )


async def help_parser(name, keyboard=None):
    if not keyboard:
        help_keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return var.help_text, help_keyboard


@app.on_callback_query(filters.regex("bot_commands"))
@languageCB
async def commands_callback(client, CallbackQuery, _):
    text, help_keyboard = await help_parser(CallbackQuery.from_user.mention)
    await CallbackQuery.message.edit(
        text=_["main5"], reply_markup=help_keyboard, disable_web_page_preview=True
    )


if __name__ == "__main__":
    install()
    with closing(loop):
        with suppress(asyncio.exceptions.CancelledError):
            loop.run_until_complete(start_bot())
