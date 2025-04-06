from database.users_chats_db import tech_vj


async def update_user_plan(user_id, plan):
    user = await tech_vj.col.find_one({'id': user_id})
    if user:
        await tech_vj.col.update_one({'id': user_id}, {'$set': {'plan': plan}})
    else:
        await tech_vj.add_user(user_id, "Unknown")
        await tech_vj.col.update_one({'id': user_id}, {'$set': {'plan': plan}})
