# lovebirds.py
# Features: Enhanced Virtual Gift System + Love Story Generator with MongoDB
# Author: Nand Yaduwanshi | Fixed by Shiv (2025)

import random
from pyrogram import filters
from ShrutiMusic import app
from ShrutiMusic.core.mongo import mongodb
from config import MONGO_DB_URI

# MongoDB collections
lovebirds_db = mongodb.lovebirds
users_collection = lovebirds_db.users
gifts_collection = lovebirds_db.gifts

# Available gifts
GIFTS = {
    "🌹": {"name": "Rose", "cost": 10, "emoji": "🌹"},
    "🍫": {"name": "Chocolate", "cost": 20, "emoji": "🍫"},
    "🧸": {"name": "Teddy Bear", "cost": 30, "emoji": "🧸"},
    "💍": {"name": "Ring", "cost": 50, "emoji": "💍"},
    "❤️": {"name": "Heart", "cost": 5, "emoji": "❤️"},
    "🌺": {"name": "Flower Bouquet", "cost": 25, "emoji": "🌺"},
    "💎": {"name": "Diamond", "cost": 100, "emoji": "💎"},
    "🎀": {"name": "Gift Box", "cost": 40, "emoji": "🎀"},
    "🌙": {"name": "Moon", "cost": 35, "emoji": "🌙"},
    "⭐️": {"name": "Star", "cost": 15, "emoji": "⭐️"},
    "🦋": {"name": "Butterfly", "cost": 18, "emoji": "🦋"},
    "🕊": {"name": "Dove", "cost": 22, "emoji": "🕊"},
    "🏰": {"name": "Castle", "cost": 80, "emoji": "🏰"},
    "🎂": {"name": "Cake", "cost": 28, "emoji": "🎂"},
    "🍓": {"name": "Strawberry", "cost": 12, "emoji": "🍓"},
}

# ---------------------- DATABASE HELPERS ----------------------

async def get_user_data(user_id: int):
    user_data = await users_collection.find_one({"user_id": user_id})
    if not user_data:
        user_data = {"user_id": user_id, "coins": 50, "total_gifts_received": 0, "total_gifts_sent": 0, "created_at": "2025"}
        await users_collection.insert_one(user_data)
    return user_data

async def update_user_coins(user_id: int, amount: int):
    await users_collection.update_one({"user_id": user_id}, {"$inc": {"coins": amount}}, upsert=True)

async def get_user_gifts(user_id: int, gift_type="received"):
    query_field = "receiver_id" if gift_type == "received" else "sender_id"
    gifts = await gifts_collection.find({query_field: user_id}).to_list(length=None)
    return gifts

# ---------------------- UTILITIES ----------------------

def get_user_info(message):
    if not message.from_user:
        return None, None
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name or "Unknown"
    return user_id, username

# ---------------------- COMMANDS ----------------------

@app.on_message(filters.command(["balance", "bal"], prefixes=["/", "!", "."]))
async def balance(_, message):
    uid, username = get_user_info(message)
    if not uid:
        return
    user_data = await get_user_data(uid)
    coins = user_data["coins"]
    gifts_received = await gifts_collection.count_documents({"receiver_id": uid})
    gifts_sent = await gifts_collection.count_documents({"sender_id": uid})
    balance_text = f"💰 <b>{username}'s Account</b>\n💸 <b>Balance:</b> {coins} coins\n🎁 <b>Gifts Received:</b> {gifts_received}\n📤 <b>Gifts Sent:</b> {gifts_sent}\n\n💡 <b>Tip:</b> Send messages to earn coins!"
    await message.reply_text(balance_text)

@app.on_message(filters.command("gifts", prefixes=["/", "!", "."]))
async def gift_list(_, message):
    text = "🎁 <b>Available Gifts:</b>\n\n"
    for emoji, gift_info in sorted(GIFTS.items(), key=lambda x: x[1]["cost"]):
        text += f"{emoji} <b>{gift_info['name']}</b> - {gift_info['cost']} coins\n"
    text += "\n📝 <b>Usage:</b> /sendgift @username GiftEmoji\n💡 <b>Example:</b> /sendgift @john 🌹"
    await message.reply_text(text)
