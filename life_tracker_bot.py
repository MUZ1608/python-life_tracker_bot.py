import telebot
from datetime import datetime, timedelta

API_TOKEN = '7920018615:AAEW93HhU3PaBj0IuPqxaq1LG7gKr0SO-Eo'

bot = telebot.TeleBot(API_TOKEN)

users = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Salom! Isming nima?")
    users[message.chat.id] = {"step": "get_name"}

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    user = users.get(message.chat.id, {})

    if user.get("step") == "get_name":
        users[message.chat.id]["name"] = message.text
        users[message.chat.id]["step"] = "get_birthdate"
        bot.reply_to(message, "📅 Tug'ilgan kuningni yoz: `YYYY-MM-DD` formatda.")

    elif user.get("step") == "get_birthdate":
        try:
            birth_date = datetime.strptime(message.text, "%Y-%m-%d")
            users[message.chat.id]["birth_date"] = birth_date
            users[message.chat.id]["step"] = "done"

            now = datetime.now()
            lived = now - birth_date
            total_life = timedelta(days=80*365.25)  # 80 yil
            remaining = total_life - lived

            lived_percent = (lived / total_life) * 100
            remaining_percent = 100 - lived_percent

            text = (
                f"👤 {users[message.chat.id]['name']}, sen {birth_date.strftime('%Y-%m-%d')} kuni tug‘ilgansan.\n\n"
                f"⏳ Yashagan vaqt: {lived.days} kun (~{lived.days // 365} yil)\n"
                f"🕰️ O‘rtacha umr (80 yil) bo‘yicha:\n"
                f"✅ Yashaganing: {lived_percent:.2f}%\n"
                f"⏱️ Qolganing: {remaining_percent:.2f}%\n"
                f"📆 Taxminiy o‘lim sanasi: {(birth_date + total_life).strftime('%Y-%m-%d')}"
            )
            bot.reply_to(message, text)

        except ValueError:
            bot.reply_to(message, "⚠️ Format noto‘g‘ri. Tug‘ilgan kunni `YYYY-MM-DD` shaklida yoz.")

    else:
        bot.reply_to(message, "👋 /start buyrug‘i bilan boshlang!")

bot.infinity_polling()
