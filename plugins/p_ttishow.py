from pyrogram import Client, filters, enums
import psutil
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong, PeerIdInvalid
from info import ADMINS, LOG_CHANNEL, SUPPORT_CHAT, MELCOW_NEW_USERS, MELCOW_VID, CHNL_LNK, GRP_LNK, GROUP_LOGS
from database.users_chats_db import db
from database.ia_filterdb import Media
from utils import get_size, temp, get_settings
from Script import script
from pyrogram.errors import ChatAdminRequired
import asyncio 

"""-----------------------------------------https://t.me/GetTGLink/4179 --------------------------------------"""

@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, message):
    r_j_check = [u.id for u in message.new_chat_members]
    if temp.ME in r_j_check:
        if not await db.get_chat(message.chat.id):
            total = await bot.get_chat_members_count(message.chat.id)
            r_j = message.from_user.mention if message.from_user else "Anonymous" 
            await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, r_j))       
            await db.add_chat(message.chat.id, message.chat.title)
        if message.chat.id in temp.BANNED_CHATS:
            # Inspired from a boat of a banana tree
            buttons = [[
                InlineKeyboardButton('Support', url=f'https://t.me/{SUPPORT_CHAT}')
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            k = await message.reply(
                text='<b>CHAT NOT ALLOWED 🐞\n\nMy admins have restricted me from working here! If you want to know more about it, contact support.</b>',
                reply_markup=reply_markup,
            )

            try:
                await k.pin()
            except:
                pass
            await bot.leave_chat(message.chat.id)
            return

        # Check the number of members in the group
        chat_info = await bot.get_chat(message.chat.id)
        member_count = chat_info.members_count

        # If the group has 200 or more members, automatically verify it
        if member_count >= 200:
            # Automatically verify the chat
            await db.verify_crazy_chat(message.chat.id)
            temp.CRAZY_VERIFIED_CHATS.append(message.chat.id)

            # Notify the group about automatic verification
            verification_text = ("<b><u> ᴠᴇʀɪꜰɪᴇᴅ ✅</u>\n\n ᴄᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴꜱ! 🎉 ᴛʜɪꜱ ɢʀᴏᴜᴘ ʜᴀꜱ ʙᴇᴇɴ "
                                "ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴠᴇʀɪꜰɪᴇᴅ. \n\n ʏᴏᴜ ᴄᴀɴ ɴᴏᴡ ᴇɴᴊᴏʏ ᴛʜᴇ ꜰᴜʟʟ ʀᴀɴɢᴇ ᴏꜰ ꜰᴇᴀᴛᴜʀᴇꜱ "
                                "ᴘʀᴏᴠɪᴅᴇᴅ ʙʏ ᴛʜᴇ ʙᴏᴛ. ɪꜰ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ Qᴜᴇꜱᴛɪᴏɴꜱ ᴏʀ ɴᴇᴇᴅ ᴀꜱꜱɪꜱᴛᴀɴᴄᴇ, "
                                "ꜰᴇᴇʟ ꜰʀᴇᴇ ᴛᴏ ᴀꜱᴋ. 😊</b>")
            
            # Generate chat invite link
            invite_link = await bot.export_chat_invite_link(message.chat.id)
            
            # Display buttons for further actions
            btn = [
                [InlineKeyboardButton("ᴅɪꜱᴀʙʟᴇ ᴄʜᴀᴛ ❌", callback_data=f"bangrpchat:{message.chat.id}")],
                [InlineKeyboardButton("ᴄʜᴀᴛ ɪɴᴠɪᴛᴇ ʟɪɴᴋ 🌐", url=invite_link)]
            ]
            
            reply_markup = InlineKeyboardMarkup(btn)

            await bot.send_message(message.chat.id, text=verification_text, reply_markup=reply_markup)
            
            # Notify the logs group about automatic verification
            await bot.send_message(GROUP_LOGS,
                                  text=("<b>#ᴠᴇʀɪꜰɪᴇᴅ\n\n<u> ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴠᴇʀɪꜰɪᴇᴅ 🔁</u> \n\n ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ʀᴇQᴜᴇꜱᴛ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴀᴄᴄᴇᴘᴛᴇᴅ ✅\n\n"
                                        "🏷️ ɢʀᴏᴜᴘ / ᴄʜᴀᴛ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ \n\n ☎️ ᴄʜᴀᴛ ɪᴅ - <code>{message.chat.id}</code>\n\n🕵️ ᴛᴏᴛᴀʟ ᴍᴇʙᴇʀꜱ - <code>{member_count}</code></b>"),
                                  reply_markup=reply_markup)

        else:
            # If the group has less than 200 members, proceed with the regular verification process
            callback_data = f"verify_crazy_group:{message.chat.id}"
            cz_buttons = [
                [
                    InlineKeyboardButton("ᴠᴇʀɪꜰʏ  ᴄʜᴀᴛ ✅", callback_data=callback_data),
                    InlineKeyboardButton("ʙᴀɴ  ᴄʜᴀᴛ 😡", callback_data=f"bangrpchat:{message.chat.id}")
                ]
            ]
            crazy_markup = InlineKeyboardMarkup(cz_buttons)
            await bot.send_message(GROUP_LOGS,
                                   text=f"<b>#ʀᴇQᴜᴇꜱᴛ\n\n<u> ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ʀᴇQᴜᴇꜱᴛ ⁉️</u>\n\n 🏷️ ɢʀᴏᴜᴘ / ᴄʜᴀᴛ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ \n\n ☎️ ᴄʜᴀᴛ ɪᴅ - <code>{message.chat.id}</code>\n\n🕵️ ᴛᴏᴛᴀʟ ᴍᴇʙᴇʀꜱ - <code>{member_count}</code> </b>",
                                   reply_markup=crazy_markup)

            # Reply to the user in the group
            await message.reply_text("<b>🔒 <u> ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ʀᴇQᴜᴇꜱᴛ ꜱᴇɴᴛ! </u> \n\n ᴡᴇ ʜᴀᴠᴇ ꜱᴜʙᴍɪᴛᴛᴇᴅ ᴀ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ʀᴇQᴜᴇꜱᴛ ꜰᴏʀ ᴛʜɪꜱ ɢʀᴏᴜᴘ. ᴘʟᴇᴀꜱᴇ ʙᴇ ᴘᴀᴛɪᴇɴᴛ ᴡʜɪʟᴇ ᴏᴜʀ ᴛᴇᴀᴍ ʀᴇᴠɪᴇᴡꜱ ᴀɴᴅ ᴀᴘᴘʀᴏᴠᴇꜱ ɪᴛ. \n\n⌛ ɪꜰ ʏᴏᴜ ᴡᴏᴜʟᴅ ʟɪᴋᴇ ᴛᴏ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴘʀᴏɢʀᴇꜱꜱ ᴏʀ ʀᴇᴄᴇɪᴠᴇ ᴜᴘᴅᴀᴛᴇꜱ ᴏɴ ᴛʜᴇ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴘʀᴏᴄᴇꜱꜱ, ʏᴏᴜ ᴄᴀɴ ᴊᴏɪɴ ᴏᴜʀ 𝗩𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝘁𝗶𝗼𝗻 𝗦𝘁𝗮𝘁𝘂𝘀 𝗖𝗵𝗮𝗻𝗻𝗲𝗹. \n\n.ᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ʏᴏᴜʀ ᴄᴏᴏᴘᴇʀᴀᴛɪᴏɴ! 🙏</b>",
                                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔺 ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ꜱᴛᴀᴛᴜꜱ ᴄʜᴀɴɴᴇʟ 🔺", url=f"https://t.me/+nkscY_k6wdk4Y2E1")],[InlineKeyboardButton('ᴄʟᴏꜱᴇ / ᴅᴇʟᴇᴛᴇ 🗑️', callback_data='close_data')]]))

    else:
        settings = await get_settings(message.chat.id)
        if settings["welcome"]:
            for u in message.new_chat_members:
                if (temp.MELCOW).get('welcome') is not None:
                    try:
                        await (temp.MELCOW['welcome']).delete()
                    except:
                        pass
                temp.MELCOW['welcome'] = await message.reply_video(
                    video=(MELCOW_VID),
                    caption=(script.MELCOW_ENG.format(u.mention, message.chat.title)),
                    reply_markup=InlineKeyboardMarkup(
                        [[
                            InlineKeyboardButton('🍁 Uᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ 🍁', url=CHNL_LNK)
                        ]]
                    ),
                    parse_mode=enums.ParseMode.HTML
                )

        if settings["auto_delete"]:
            await asyncio.sleep(600)
            await (temp.MELCOW['welcome']).delete()
                
               
@Client.on_message(filters.command('leave') & filters.user(ADMINS))
async def leave_a_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        chat = chat
    try:
        buttons = [[
            InlineKeyboardButton('Owner', url="https://t.me/heartlesssn")
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat,
            text='<b>Hello Friends, \nMy admin has told me to leave from group, so i go! If you wanna add me again contact my Support Group or My Owner</b>',
            reply_markup=reply_markup,
        )

        await bot.leave_chat(chat)
        await message.reply(f"left the chat `{chat}`")
    except Exception as e:
        await message.reply(f'Error - {e}')

@Client.on_message(filters.command('disable') & filters.user(ADMINS))
async def disable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat_ = int(chat)
    except:
        return await message.reply('Give Me A Valid Chat ID')
    cha_t = await db.get_chat(int(chat_))
    if not cha_t:
        return await message.reply("Chat Not Found In DB")
    if cha_t['is_disabled']:
        return await message.reply(f"This chat is already disabled:\nReason-<code> {cha_t['reason']} </code>")
    await db.disable_chat(int(chat_), reason)
    temp.BANNED_CHATS.append(int(chat_))
    await message.reply('Chat Successfully Disabled')
    try:
        buttons = [[
            InlineKeyboardButton('Support', url="https://t.me/heartlesssn")
        ]]
        reply_markup=InlineKeyboardMarkup(buttons)
        await bot.send_message(
            chat_id=chat_, 
            text=f'<b>Hello Friends, \nMy admin has told me to leave from group so i go! If you wanna add me again contact my support group.</b> \nReason : <code>{reason}</code>',
            reply_markup=reply_markup)
        await bot.leave_chat(chat_)
    except Exception as e:
        await message.reply(f"Error - {e}")


@Client.on_message(filters.command('enable') & filters.user(ADMINS))
async def re_enable_chat(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat_ = int(chat)
    except:
        return await message.reply('Give Me A Valid Chat ID')
    sts = await db.get_chat(int(chat))
    if not sts:
        return await message.reply("Chat Not Found In DB !")
    if not sts.get('is_disabled'):
        return await message.reply('This chat is not yet disabled.')
    await db.re_enable_chat(int(chat_))
    temp.BANNED_CHATS.remove(int(chat_))
    await message.reply("Chat Successfully re-enabled")


@Client.on_message(filters.command('stats') & filters.user(ADMINS) & filters.incoming)
async def get_ststs(bot, message):
    buttons = [[
            InlineKeyboardButton('✘ ᴄʟᴏsᴇ ✘', callback_data='close_data')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    kdbotz = await message.reply('Fetching stats..')
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    total_users = await db.total_users_count()
    totl_chats = await db.total_chat_count()
    files = await Media.count_documents()
    size = await db.get_db_size()
    free = 536870912 - size
    size = get_size(size)
    free = get_size(free)
    await kdbotz.edit_text(
            text=script.ADMIN_STATUS_TXT.format(cpu, ram, files, total_users, totl_chats, size, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )


@Client.on_message(filters.command('invite') & filters.user(ADMINS))
async def gen_invite(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a chat id')
    chat = message.command[1]
    try:
        chat = int(chat)
    except:
        return await message.reply('Give Me A Valid Chat ID')
    try:
        link = await bot.create_chat_invite_link(chat)
    except ChatAdminRequired:
        return await message.reply("Invite Link Generation Failed, Iam Not Having Sufficient Rights")
    except Exception as e:
        return await message.reply(f'Error {e}')
    await message.reply(f'Here is your Invite Link {link.invite_link}')

@Client.on_message(filters.command('ban') & filters.user(ADMINS))
async def ban_a_user(bot, message):
    # https://t.me/GetTGLink/4185
    if len(message.command) == 1:
        return await message.reply('Give me a user id / username')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("This is an invalid user, make sure ia have met him before.")
    except IndexError:
        return await message.reply("This might be a channel, make sure its a user.")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if jar['is_banned']:
            return await message.reply(f"{k.mention} is already banned\nReason: {jar['ban_reason']}")
        await db.ban_user(k.id, reason)
        temp.BANNED_USERS.append(k.id)
        await message.reply(f"Successfully banned {k.mention}")


    
@Client.on_message(filters.command('unban') & filters.user(ADMINS))
async def unban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('Give me a user id / username')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "No reason Provided"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("This is an invalid user, make sure ia have met him before.")
    except IndexError:
        return await message.reply("Thismight be a channel, make sure its a user.")
    except Exception as e:
        return await message.reply(f'Error - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if not jar['is_banned']:
            return await message.reply(f"{k.mention} is not yet banned.")
        await db.remove_ban(k.id)
        temp.BANNED_USERS.remove(k.id)
        await message.reply(f"Successfully unbanned {k.mention}")


    
@Client.on_message(filters.command('users') & filters.user(ADMINS))
async def list_users(bot, message):
    # https://t.me/GetTGLink/4184
    raju = await message.reply('Getting List Of Users')
    users = await db.get_all_users()
    out = "Users Saved In DB Are:\n\n"
    async for user in users:
        out += f"<a href=tg://user?id={user['id']}>{user['name']}</a>"
        if user['ban_status']['is_banned']:
            out += '( Banned User )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('users.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('users.txt', caption="List Of Users")

@Client.on_message(filters.command('chats') & filters.user(ADMINS))
async def list_chats(bot, message):
    raju = await message.reply('Getting List Of chats')
    chats = await db.get_all_chats()
    out = "Chats Saved In DB Are:\n\n"
    async for chat in chats:
        if not chat['chat_status']['is_disabled']:
            out += f"**Title:** `{chat['title']}`\n**- ID:** `{chat['id']}`\n" 
            # Additional logic to include whether the chat is disabled
            if chat['chat_status']['is_disabled']:
                out += '( Disabled Chat )\n'     
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('chats.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('chats.txt', caption="List Of Chats")
        await db.remove_disabled_chats()

