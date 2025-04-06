
from datetime import datetime, timedelta
from vjupbot_test.plans import PLANS

# ساختار نمونه برای کاربران
users_data = {}

def get_user_data(user_id):
    if user_id not in users_data:
        users_data[user_id] = {
            "plan": "free",
            "plan_start": datetime.utcnow(),
            "last_upload_time": None,
            "daily_uploaded": 0,
            "daily_reset": datetime.utcnow().date()
        }
    return users_data[user_id]

def update_upload_usage(user_id, bytes_uploaded):
    user = get_user_data(user_id)
    today = datetime.utcnow().date()
    if user["daily_reset"] != today:
        user["daily_uploaded"] = 0
        user["daily_reset"] = today
    user["daily_uploaded"] += bytes_uploaded
    user["last_upload_time"] = datetime.utcnow()

def is_plan_expired(user_id):
    user = get_user_data(user_id)
    plan_obj = PLANS[user["plan"]]
    if not plan_obj.duration:
        return False
    return datetime.utcnow() > user["plan_start"] + plan_obj.duration

def reset_to_free_if_expired(user_id):
    if is_plan_expired(user_id):
        users_data[user_id]["plan"] = "free"
        users_data[user_id]["plan_start"] = datetime.utcnow()
        return True  # پلن تغییر کرد
    return False


# کد قبلی:
# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import motor.motor_asyncio
from config import Config

DATABASE_NAME = "vjbotztechvj"
DATABASE_URI = Config.TECH_VJ_DATABASE_URL

class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.grp = self.db.groups


    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
        )


    def new_group(self, id, title):
        return dict(
            id = id,
            title = title,
            chat_status=dict(
                is_disabled=False,
                reason="",
            ),
        )
    
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return bool(user)
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
    
    

    async def get_all_users(self):
        return self.col.find({})
    

    


    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']


tech_vj = Database(DATABASE_URI, DATABASE_NAME)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
