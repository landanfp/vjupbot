# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

from pyrogram import Client as Tech_VJ
from pyrogram import filters, enums
from config import Config
from database.access import techvj
from plugins.buttons import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

# دکمه‌های ارتقا به پلن نقره ای و طلایی
@Tech_VJ.on_message(filters.command("add_pro"))
async def add_pro(client: Tech_VJ, message: Message):
    if message.from_user.id != Config.TECH_VJ_OWNER_ID:
        return

    user_id = int(message.text.split()[1])

    buttons = [
        [InlineKeyboardButton("Upgrade to Silver Plan", callback_data=f"upgrade_silver_{user_id}")],
        [InlineKeyboardButton("Upgrade to Gold Plan", callback_data=f"upgrade_gold_{user_id}")],
    ]
    await message.reply("Choose a plan to upgrade:", reply_markup=InlineKeyboardMarkup(buttons))


# مدیریت ارتقا به پلن نقره ای و طلایی
@Tech_VJ.on_callback_query()
async def handle_upgrade(client: Tech_VJ, callback_query):
    user_id = int(callback_query.data.split("_")[2])
    plan = "silver" if "silver" in callback_query.data else "gold"

    await update_user_plan(user_id, plan)
    await callback_query.message.edit_text(f"User {user_id} has been upgraded to {plan.capitalize()} Plan.")


# دستور remove_pro برای بازگشت به پلن رایگان
@Tech_VJ.on_message(filters.command("remove_pro"))
async def remove_pro(client: Tech_VJ, message: Message):
    if message.from_user.id != Config.TECH_VJ_OWNER_ID:
        return

    user_id = int(message.text.split()[1])
    await update_user_plan(user_id, "free")
    await message.reply(f"User {user_id} has been downgraded to Free Plan.")


# دستور bun برای بستن دسترسی کاربر
@Tech_VJ.on_message(filters.command("bun"))
async def ban_user(client: Tech_VJ, message: Message):
    if message.from_user.id != Config.TECH_VJ_OWNER_ID:
        return

    user_id = int(message.text.split()[1])

    # بستن دسترسی کاربر
    await techvj.col.update_one({'id': user_id}, {'$set': {'ban_status.is_banned': True}})
    await message.reply(f"User {user_id} has been banned.")


# دستور unbun برای رفع قطع دسترسی
@Tech_VJ.on_message(filters.command("unbun"))
async def unban_user(client: Tech_VJ, message: Message):
    if message.from_user.id != Config.TECH_VJ_OWNER_ID:
        return

    user_id = int(message.text.split()[1])

    # آزادسازی دسترسی کاربر
    await techvj.col.update_one({'id': user_id}, {'$set': {'ban_status.is_banned': False}})
    await message.reply(f"User {user_id} has been unbanned.")


# دستور total برای مشاهده تعداد کاربران
@Tech_VJ.on_message(filters.private & filters.command('total'))
async def sts(c, m):
    if m.from_user.id != Config.TECH_VJ_OWNER_ID:
        return 
    total_users = await techvj.total_users_count()
    await m.reply_text(text=f"Total user(s) {total_users}", quote=True)


# دستور search برای جستجوی تورنت
@Tech_VJ.on_message(filters.private & filters.command("search"))
async def serc(bot, update):
    await bot.send_message(chat_id=update.chat.id, text="🔍 TORRENT SEARCH", 
    parse_mode=enums.ParseMode.HTML, reply_markup=Button.BUTTONS01)


# دستور update_user_plan برای تغییر وضعیت پلن
async def update_user_plan(user_id, plan):
    await techvj.col.update_one({'id': user_id}, {'$set': {'plan': plan}})
