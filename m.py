#!/usr/bin/env python3

import telebot
import datetime
import os

# =========================
# BOT TOKEN
# =========================
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

bot = telebot.TeleBot(BOT_TOKEN)

# =========================
# ADMIN IDS
# =========================
ADMIN_IDS = ["7178871598"]

# =========================
# FILES
# =========================
USER_FILE = "users.txt"
LOG_FILE = "logs.txt"

# =========================
# READ USERS
# =========================
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

allowed_users = read_users()

# =========================
# SAVE USER
# =========================
def save_user(user_id):
    with open(USER_FILE, "a") as file:
        file.write(f"{user_id}\n")

# =========================
# LOG FUNCTION
# =========================
def save_log(text):
    with open(LOG_FILE, "a") as file:
        file.write(text + "\n")

# =========================
# START COMMAND
# =========================
@bot.message_handler(commands=['start'])
def start_command(message):
    name = message.from_user.first_name

    response = f"Hello {name}! 👋\n\nSafe Telegram Bot Running Successfully ✅"

    bot.reply_to(message, response)

# =========================
# HELP COMMAND
# =========================
@bot.message_handler(commands=['help'])
def help_command(message):
    response = """
📌 Available Commands:

/start - Start bot
/help - Show commands
/myinfo - Your info
/adduser - Admin add user
/allusers - Show all users
/logs - Show logs
"""

    bot.reply_to(message, response)

# =========================
# MY INFO
# =========================
@bot.message_handler(commands=['myinfo'])
def myinfo_command(message):
    user_id = str(message.chat.id)

    user_info = bot.get_chat(user_id)

    username = user_info.username if user_info.username else "No Username"

    role = "Admin" if user_id in ADMIN_IDS else "User"

    response = f"""
👤 User Info

🆔 ID: {user_id}
👤 Username: {username}
🔖 Role: {role}
"""

    bot.reply_to(message, response)

# =========================
# ADD USER
# =========================
@bot.message_handler(commands=['adduser'])
def add_user(message):
    user_id = str(message.chat.id)

    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "❌ Only admin can use this command")
        return

    command = message.text.split()

    if len(command) != 2:
        bot.reply_to(message, "Usage: /adduser USER_ID")
        return

    new_user = command[1]

    if new_user in allowed_users:
        bot.reply_to(message, "User already exists")
        return

    allowed_users.append(new_user)
    save_user(new_user)

    bot.reply_to(message, f"✅ User {new_user} added successfully")

# =========================
# ALL USERS
# =========================
@bot.message_handler(commands=['allusers'])
def all_users(message):
    user_id = str(message.chat.id)

    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "❌ Admin only command")
        return

    if not allowed_users:
        bot.reply_to(message, "No users found")
        return

    text = "📋 Users List:\n\n"

    for uid in allowed_users:
        text += f"• {uid}\n"

    bot.reply_to(message, text)

# =========================
# LOGS COMMAND
# =========================
@bot.message_handler(commands=['logs'])
def logs_command(message):
    user_id = str(message.chat.id)

    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "❌ Admin only command")
        return

    if not os.path.exists(LOG_FILE):
        bot.reply_to(message, "No logs found")
        return

    with open(LOG_FILE, "rb") as file:
        bot.send_document(message.chat.id, file)

# =========================
# MESSAGE LOGGER
# =========================
@bot.message_handler(func=lambda m: True)
def all_messages(message):
    user_id = message.chat.id
    text = message.text

    log = f"[{datetime.datetime.now()}] {user_id}: {text}"

    save_log(log)

    bot.reply_to(message, "Message received ✅")

# =========================
# START POLLING
# =========================
print("Bot Started...")
bot.infinity_polling()
