from datetime import timedelta
import pytz
import datetime, time
from Script import script 
from info import ADMINS, PREMIUM_LOGS
from utils import get_seconds
from database.users_chats_db import db 
from pyrogram import Client, filters 
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.types import CallbackQuery
from pyrogram.types import Message

@Client.on_message(filters.command("remove_premium") & filters.user(ADMINS))
async def remove_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])  # Convert the user_id to integer
        user = await client.get_users(user_id)
        if await db.remove_premium_access(user_id):
            await message.reply_text("**ᴜꜱᴇʀ ʜᴀꜱ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴛʀᴀɴꜱɪᴛɪᴏɴᴇᴅ ᴏᴜᴛ ᴏꜰ ᴛʜᴇ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ...❌**")
            await client.send_message(
                chat_id=user_id,
                text=f"<b>ʜᴀʏ {user.mention}, 👋\n\nʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ : ᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴜsɪɴɢ ᴏᴜʀ sᴇʀᴠɪᴄᴇ 😊</b>"
            )
        else:
            await message.reply_text("**ᴜɴᴀʙʟᴇ ᴛᴏ ʀᴇᴍᴏᴠᴇ, ᴀʀᴇ ʏᴏᴜ ꜱᴜʀᴇ ɪᴛ ᴡᴀꜱ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ɪᴅ ⁉️**")
    else:
        await message.reply_text("<b><u>🛠️ ɪɴᴄᴏᴍᴘʟᴇᴛᴇ ᴄᴏᴍᴍᴀɴᴅ:</u>\n\n👉 `/remove_premium user_id`</b>") 

@Client.on_message(filters.command("myplan"))
async def myplan(client, message):
    user = message.from_user.mention 
    user_id = message.from_user.id
    data = await db.get_user(message.from_user.id)  # Convert the user_id to integer
    if data and data.get("expiry_time"):
        #expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=data)
        expiry = data.get("expiry_time") 
        expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y  ⏰: %I:%M:%S %p")            
        # Calculate time difference
        current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        time_left = expiry_ist - current_time
            
        # Calculate days, hours, and minutes
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
            
        # Format time left as a string
        time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
        await message.reply_text(f"<b><u>ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ɪꜱ ᴀᴄᴛɪᴠᴇ. ✅</u>\n\n👤 ʏᴏᴜʀ ɴᴀᴍᴇ : {user}\n\n❗ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n\n⏰ ᴛɪᴍᴇ ʟᴇꜰᴛ : <code>{time_left_str}</code>\n\n⌛️ ᴇxᴘɪʀʏ: <code>{expiry_str_in_ist}</code>.</b>")   
    else:
        await message.reply_text(f"**ʜᴀʏ {user}.., 👋\n\nʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴʏ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ, ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴛᴀᴋᴇ ᴘʀᴇᴍɪᴜᴍ ᴛʜᴇɴ\nᴄʟɪᴄᴋ ᴏɴ /plan ᴛᴏ ᴋɴᴏᴡ ᴀʙᴏᴜᴛ ᴛʜᴇ ᴘʟᴀɴ**")

@Client.on_message(filters.command("get_premium") & filters.user(ADMINS))
async def get_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        data = await db.get_user(user_id)  # Convert the user_id to integer
        if data and data.get("expiry_time"):
            #expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=data)
            expiry = data.get("expiry_time") 
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y %I:%M:%S %p")            
            # Calculate time difference
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            
            # Calculate days, hours, and minutes
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            # Format time left as a string
            time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
            await message.reply_text(f"<b><u>ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ɪꜱ ᴀᴄᴛɪᴠᴇ. ✅</u>\n\n👤 ᴜꜱᴇʀ ɴᴀᴍᴇ: {user.mention}\n\n❗ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n\n⏰ ᴛɪᴍᴇ ʟᴇꜰᴛ : <code>{time_left_str}</code>\n\n⌛️ ᴇxᴘɪʀʏ: <code>{expiry_str_in_ist}</code>.</b>")
        else:
            await message.reply_text("**ɴᴏ ᴘʀᴇᴍɪᴜᴍ ᴅᴀᴛᴀ ᴏꜰ ᴛʜᴇ ᴜꜱᴇʀ ᴡᴀꜱ ꜰᴏᴜɴᴅ ɪɴ ᴛʜᴇ ᴅᴀᴛᴀʙᴀꜱᴇ ❗**")
    else:
        await message.reply_text("<b><u>🛠️ ɪɴᴄᴏᴍᴘʟᴇᴛᴇ ᴄᴏᴍᴍᴀɴᴅ:</u>\n\n👉 `/get_premium user_id`</b>")

@Client.on_message(filters.command("add_premium") & filters.user(ADMINS))
async def give_premium_cmd_handler(client, message):
    if len(message.command) == 4:
        time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        current_time = time_zone.strftime("%d-%m-%Y  ⏰: %I:%M:%S %p") 
        user_id = int(message.command[1])  # Convert the user_id to integer
        user = await client.get_users(user_id)
        time = message.command[2]+" "+message.command[3]
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            user_data = {"id": user_id, "expiry_time": expiry_time}  # Using "id" instead of "user_id"  
            await db.update_user(user_data)  # Use the update_user method to update or insert user data
            data = await db.get_user(user_id)
            expiry = data.get("expiry_time")   
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y  ⏰: %I:%M:%S %p")         
            await message.reply_text(f"<u>𝙋𝙧𝙚𝙢𝙞𝙪𝙢 𝙖𝙘𝙘𝙚𝙨𝙨 𝙖𝙙𝙙𝙚𝙙 𝙩𝙤 𝙩𝙝𝙚 𝙪𝙨𝙚𝙧 ✅</u>\n\n<b>👤 ᴜꜱᴇʀ ɴᴀᴍᴇ : {user.mention}\n\n❗ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ ᴛɪᴍᴇ : <code>{time}</code>\n\n🔐 ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ : <code>{current_time}</code>\n\n⌛️ ᴇxᴘɪʀʏ: <code>{expiry_str_in_ist}</code>.</b>", disable_web_page_preview=True)
            await client.send_message(
                chat_id=user_id,
                text=f"𝗛𝗮𝘆 {user.mention}\n\n<u>𝗬𝗼𝘂𝗿 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝘀𝘂𝗯𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 𝗶𝘀 𝗻𝗼𝘄 𝗮𝗰𝘁𝗶𝘃𝗲. 𝗦𝘁𝗮𝗿𝘁 𝗲𝗻𝗷𝗼𝘆𝗶𝗻𝗴 𝗮𝗹𝗹 𝘁𝗵𝗲 𝗯𝗲𝗻𝗲𝗳𝗶𝘁𝘀! 🎉</u>\n\n<b>⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ ᴛɪᴍᴇ : <code>{time}</code>\n\n🔐 ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ : <code>{current_time}</code>\n\n⌛️ ᴇxᴘɪʀʏ: <code>{expiry_str_in_ist}</code></b>", disable_web_page_preview=True              
            )    
            await client.send_message(PREMIUM_LOGS, text=f"<b>#added_Premium\n\n👤 ᴜꜱᴇʀ ɴᴀᴍᴇ : {user.mention}\n\n❗ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ ᴛɪᴍᴇ : <code>{time}</code>\n\n🔐 ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ : <code>{current_time}</code>\n\n⌛️ ᴇxᴘɪʀʏ: <code>{expiry_str_in_ist}</code></b>", disable_web_page_preview=True)
                    
        else:
            await message.reply_text("Invalid time format. Please use '1 day for days', '1 hour for hours', or '1 min for minutes', or '1 month for months' or '1 year for year'")
    else:
        await message.reply_text("<b><u>🛠️ ɪɴᴄᴏᴍᴘʟᴇᴛᴇ ᴄᴏᴍᴍᴀɴᴅ:</u>\n\n 👉 /add_premium user_id time (e.g., '1 day for days', '1 hour for hours', or '1 min for minutes', or '1 month for months' or '1 year for year')</b>")

@Client.on_message(filters.command("premium_user") & filters.user(ADMINS))
async def premium_user(client, message):
    aa = await message.reply_text("**ꜰᴇᴛᴄʜɪɴɢ ...**")
    new = f"<b><u>Paid Users</u></b> - \n\n"
    user_count = 1
    users = await db.get_all_users()
    async for user in users:
        data = await db.get_user(user['id'])
        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time") 
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y %I:%M:%S %p")            
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left_str = f"**{days} days, {hours} hours, {minutes} minutes**"	 
            new += f"**{user_count}. User ID: {user['id']}\nName: {(await client.get_users(user['id'])).mention}\nExpiry Date: {expiry_str_in_ist}\nExpiry Time: {time_left_str}**\n\n"
            user_count += 1
        else:
            pass
    try:    
        await aa.edit_text(new)
    except MessageTooLong:
        with open('usersplan.txt', 'w+') as outfile:
            outfile.write(new)
        await message.reply_document('usersplan.txt', caption="Paid Users:")



@Client.on_message(filters.command('plan') & filters.incoming)
async def plan(client, message):
    user_id = message.from_user.id 
    users = message.from_user.mention 
    btn = [[
	
        InlineKeyboardButton("📲 ꜱᴇɴᴅ ᴘᴀʏᴍᴇɴᴛ ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ʜᴇʀᴇ", user_id=int(6133992240))],[InlineKeyboardButton("❌ ᴄʟᴏsᴇ ❌", callback_data="close_data")
    ]]
    await message.reply_photo(photo="https://graph.org/file/e67318b9ea28c7b9dcb69.jpg", caption=script.PREMIUM_TEXT.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(btn))
