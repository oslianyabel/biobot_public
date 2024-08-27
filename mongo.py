import os
from pymongo import MongoClient

MONGO_URI = os.getenv('DATABASE_URL')
client = MongoClient(MONGO_URI)
db = client['wa_biomag']
admin_users_collection = db['admin_users']
conversations = db['conversations']
bot_numbers = db['bot_numbers']

def get_user_name(number):
    user = admin_users_collection.find_one({"number": number})
    if user:
        return user["name"]
    else:
        return None
    
def get_conversation(number):
    conversation = conversations.find_one({"number": number})
    if conversation:
        return conversation["messages"]
    else:
        return []
    
def get_admin_users():
    cursor = admin_users_collection.find()
    users = [row['number'] for row in cursor]
    return users
    

def update_conversation(number, messages):
    conversations.update_one(
        {"number": number},
        {"$set": {"messages": messages}},
        upsert=True
    )
    
def get_bot_number():
    result = bot_numbers.find_one({"name": "online"})

    if result:
        number = result.get("number")
        #print(f"El número es: {number}")
        return number
    else:
        print("No se encontró el número online")
        return "13145978086"