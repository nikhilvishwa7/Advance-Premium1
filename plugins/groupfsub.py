from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.users_chats_db import db
from utils import save_group_settings, get_settings
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from pyrogram import enums
from info import ADMINS

@Client.on_message(filters.group & filters.command("fsub"))
async def f_sub_cmd(bot, message):
    m = await message.reply("Please wait..")

    chat_type = message.chat.type
    
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("<b>Use this command in your group.</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and str(userid) not in ADMINS:
        await message.reply_text("<b>Only group owner can use this command 😂</b>")
        return

    try:
        f_sub = int(message.command[1])
    except (IndexError, ValueError):
        return await m.edit("<b>❌ Incorrect format!\nUse `/fsub ChannelID`</b>")

    try:
        c_link = await bot.export_chat_invite_link(grpid)
    except Exception as e:
        text = f"❌ Error: `{str(e)}`\n\nMake sure I'm admin in that channel & this group with all permissions"
        return await m.edit(text)

    await save_group_settings(grpid, 'f_sub', f_sub)
    await m.edit(f"<b>✅ Successfully Attached ForceSub to [{title}]({c_link})!</b>", disable_web_page_preview=True)

@Client.on_message(filters.group & filters.command("remove_fsub"))
async def remove_fsub_cmd(bot, message):
    m = await message.reply("Please wait..")

    chat_type = message.chat.type
    
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("<b>Use this command in your group.</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and str(userid) not in ADMINS:
        await message.reply_text("<b>Only group owner can use this command 😂</b>")
        return
    try:
        await save_group_settings(grpid, 'f_sub', None)
        await m.edit(f"<b>✅ Successfully removed ForceSub from [{title}]!</b>")
    except Exception as e:
        await m.edit(f"❌ Error: `{str(e)}`")


@Client.on_message(filters.group & filters.command("fsub_info"))
async def fsub_info_cmd(bot, message):
    m = await message.reply("Fetching ForceSub information...")

    chat_type = message.chat.type
    
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("<b>Use this command in your group.</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and str(userid) not in ADMINS:
        await m.edit("<b>Only the group owner can use this command.</b>")
        return

    settings = await get_settings(grpid)
    f_sub = settings.get('f_sub')

    if f_sub is None:
        await m.edit("<b>No ForceSub group is associated with this chat.</b>")
    else:
        try:
            # Get information about the ForceSub channel
            chat_info = await Client.get_chat(f_sub)
            chat_title = chat_info.title
            chat_invite_link = await Client.export_chat_invite_link(f_sub)
            
            await m.edit(
                f"<b>ForceSub group ID associated with this chat: {f_sub}</b>\n"
                f"<b>Name:</b> {chat_title}\n"
                f"<b>Invite Link:</b> {chat_invite_link}"
            )
        except Exception as e:
            await m.edit(f"<b>Error fetching information: {str(e)}</b>")
