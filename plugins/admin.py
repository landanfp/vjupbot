# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

from pyrogram import Client as Tech_VJ
from pyrogram import filters, enums
from config import Config
from database.access import techvj
from plugins.buttons import *

@Tech_VJ.on_message(filters.private & filters.command('total'))
async def sts(c, m):
    if m.from_user.id != Config.TECH_VJ_OWNER_ID:
        return 
    total_users = await techvj.total_users_count()
    await m.reply_text(text=f"Total user(s) {total_users}", quote=True)


@Tech_VJ.on_message(filters.private & filters.command("search"))
async def serc(bot, update):

      await bot.send_message(chat_id=update.chat.id, text="🔍 TORRENT SEARCH", 
      parse_mode=enums.ParseMode.HTML, reply_markup=Button.BUTTONS01)



from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from database.users_chats_db import get_user_data
from vjupbot_test.plans import PLANS

ADMINS = [123456789]  # شناسه ادمین‌ها (اینجا باید ID خودت رو بذاری)

@app.on_message(filters.command("addpro") & filters.user(ADMINS))
async def add_pro_handler(client, message):
    if len(message.command) != 2:
        await message.reply_text("استفاده صحیح: /addpro user_id")
        return

    user_id = message.command[1]
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("ارتقا به پلن نقره‌ای", callback_data=f"upgrade:{user_id}:silver")],
        [InlineKeyboardButton("ارتقا به پلن طلایی", callback_data=f"upgrade:{user_id}:gold")],
        [InlineKeyboardButton("ارتقا به پلن الماسی", callback_data=f"upgrade:{user_id}:diamond")]
    ])
    await message.reply_text(f"پلن موردنظر را برای کاربر {user_id} انتخاب کنید:", reply_markup=keyboard)

@app.on_callback_query(filters.regex(r"upgrade:(\d+):(silver|gold|diamond)") & filters.user(ADMINS))
async def upgrade_plan_callback(client, callback_query):
    user_id, plan_name = callback_query.data.split(":")[1:]
    user_data = get_user_data(int(user_id))
    user_data["plan"] = plan_name
    user_data["plan_start"] = datetime.utcnow()
    await callback_query.answer()
    await callback_query.message.edit_text(f"پلن کاربر {user_id} به {plan_name} ارتقا یافت.")



@app.on_callback_query(filters.regex(r"upgrade:(\d+):(silver|gold|diamond)") & filters.user(ADMINS))
async def upgrade_plan_callback(client, callback_query):
    user_id, plan_name = callback_query.data.split(":")[1:]
    user_data = get_user_data(int(user_id))
    user_data["plan"] = plan_name
    user_data["plan_start"] = datetime.utcnow()
    await callback_query.answer()
    await callback_query.message.edit_text(f"پلن کاربر {user_id} به {plan_name} ارتقا یافت.")

    # ارسال پیام به کاربر
    try:
        await client.send_message(
            int(user_id),
            f"پلن شما با موفقیت به پلن {plan_name} ارتقا یافت."
        )
    except Exception as e:
        print(f"خطا در ارسال پیام به کاربر: {e}")



from pyrogram import Client, filters
from pyrogram.types import Message
from database.users_chats_db import get_user_data, save_user_data
from datetime import datetime

@app.on_message(filters.command("remove_pro") & filters.user(ADMINS))
async def remove_pro_handler(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("لطفاً آیدی عددی کاربر را وارد کنید. مثال:\n /remove_pro 123456789")
        return

    try:
        user_id = int(message.command[1])
        user_data = get_user_data(user_id)
        user_data["plan"] = "free"
        user_data["plan_start"] = None
        save_user_data(user_id, user_data)
        await message.reply_text(f"پلن کاربر {user_id} به رایگان تغییر یافت.")
        await client.send_message(user_id, "پلن شما به پلن رایگان تغییر یافت.")
    except Exception as e:
        await message.reply_text(f"خطا: {e}")



from pyrogram import Client, filters
from pyrogram.types import Message

blacklist_file = "vjupbot-test/blacklist.txt"

@app.on_message(filters.command("add_blacksite") & filters.user(ADMINS))
async def add_blacksite_handler(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("لطفاً دامنه ممنوعه را وارد کنید. مثال:
/add_blacksite tushy.com")
        return

    domain = message.command[1].lower()
    try:
        with open(blacklist_file, "r+", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]
            if domain in lines:
                await message.reply_text(f"{domain} قبلاً در لیست وجود دارد.")
                return
            f.write(f"{domain}
")
        await message.reply_text(f"{domain} با موفقیت به لیست سایت‌های ممنوعه اضافه شد.")
    except Exception as e:
        await message.reply_text(f"خطا در افزودن دامنه: {e}")



@app.on_message(filters.command("list_blacksite") & filters.user(ADMINS))
async def list_blacksite_handler(client: Client, message: Message):
    try:
        with open(blacklist_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        if not lines:
            await message.reply_text("لیست سایت‌های ممنوعه خالی است.")
        else:
            text = "\n".join(f"{i+1}. {d}" for i, d in enumerate(lines))
            await message.reply_text("لیست سایت‌های ممنوعه:
" + text)
    except Exception as e:
        await message.reply_text(f"خطا در خواندن لیست: {e}")


@app.on_message(filters.command("remove_blacksite") & filters.user(ADMINS))
async def remove_blacksite_handler(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("لطفاً دامنه‌ای که می‌خواهید حذف شود را وارد کنید. مثال:
/remove_blacksite tushy.com")
        return

    domain = message.command[1].lower()
    try:
        with open(blacklist_file, "r+", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]
            if domain not in lines:
                await message.reply_text(f"{domain} در لیست نیست.")
                return
            lines.remove(domain)
            f.seek(0)
            f.truncate()
            f.write("\n".join(lines) + "\n")
        await message.reply_text(f"{domain} با موفقیت از لیست ممنوعه حذف شد.")
    except Exception as e:
        await message.reply_text(f"خطا در حذف دامنه: {e}")
