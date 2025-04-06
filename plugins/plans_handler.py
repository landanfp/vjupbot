
from pyrogram import Client, filters
from pyrogram.types import Message
from database.users_chats_db import get_user_data
from vjupbot_test.plans import PLANS
from datetime import datetime, timedelta

@app.on_message(filters.command("my_plan"))
async def my_plan_handler(client: Client, message: Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    plan_key = user_data["plan"]
    plan = PLANS[plan_key]
    
    name = message.from_user.first_name
    daily_used = user_data["daily_uploaded"]
    daily_limit = plan.daily_limit_bytes
    remaining = daily_limit - daily_used if daily_used < daily_limit else 0

    # تبدیل بایت به گیگابایت
    def format_size(b):
        return f"{b / (1024**3):.2f} GB"

    # درصد مصرف
    percent_used = (daily_used / daily_limit) * 100 if daily_limit > 0 else 0

    # نوار وضعیت
    def make_progress_bar(percent):
        total_blocks = 10
        filled_blocks = int((percent / 100) * total_blocks)
        empty_blocks = total_blocks - filled_blocks
        return "█" * filled_blocks + "░" * empty_blocks

    bar = make_progress_bar(percent_used)

    # تاریخ انقضا
    if plan_key == "free":
        expiry_text = "نامحدود (پلن رایگان)"
    else:
        start = user_data.get("plan_start")
        if start:
            expiry = start + timedelta(seconds=plan.duration_sec)
            expiry_text = expiry.strftime('%Y-%m-%d %H:%M')
        else:
            expiry_text = "نامشخص"

    text = f"""نام: {name}
آیدی عددی: {user_id}
نام پلن فعلی: {plan_key}
حجم پلن: {format_size(daily_limit)}
حجم استفاده شده پلن: {format_size(daily_used)} ({percent_used:.2f}% مصرف شده)
نوار وضعیت: [{bar}]
حجم باقی مانده پلن: {format_size(remaining)}
تاریخ اتمام پلن: {expiry_text}
"""
    await message.reply_text(text)
