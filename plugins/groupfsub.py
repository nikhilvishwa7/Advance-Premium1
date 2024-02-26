from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.users_chats_db import db
from utils import save_group_settings, get_settings
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from pyrogram import enums
from info import ADMINS
from pyrogram.types import *

@Client.on_message(filters.command("set_fsub"))
async def setfsub(bot, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"<b>You are anonymous admin. Turn off anonymous admin and try again this command</b>")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("<b>This Command Work Only in group\n\nTry it in your own group</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and str(userid) not in ADMINS:
        return

    try:
        f_sub = int(message.command[1])
    except (IndexError, ValueError):
        return await message.reply_text("<b>❌ Incorrect format!\nUse `/fsub ChannelID`</b>")

    try:
        c_link = await bot.export_chat_invite_link(grpid)
    except Exception as e:
        text = f"❌ Error: `{str(e)}`\n\nMake sure I'm admin in that channel & this group with all permissions"
        return await message.reply_text(text)

    await save_group_settings(grpid, 'f_sub', f_sub)
    await message.reply_text(f"<b>✅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴛᴛᴀᴄʜᴇᴅ ꜰᴏʀᴄᴇꜱᴜʙ ᴛᴏ [{title}]({c_link})!\n\n➥ ꜰᴏʀᴄᴇꜱᴜʙ ᴄʜᴀɴɴᴇʟ ☞  <code>{f_sub}</code></b>", disable_web_page_preview=True)


@Client.on_message(filters.command("remove_fsub"))
async def removetufsb(bot, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Turn off anonymous admin and try again this command")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("This Command Work Only in group\n\nTry it in your own group")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return
    else:
        pass
    reply = await message.reply_text("<b>Please Wait...</b>")
    await save_group_settings(grpid, 'f_sub', None)
    await reply.edit_text(f"<b>✧ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ʏᴏᴜʀ ꜰᴏʀᴄᴇꜱᴜʙ ᴄʜᴀɴɴᴇʟ !!!</b>")
