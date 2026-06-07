import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("♟️ Shahmat", callback_data="chess"),
         InlineKeyboardButton("🔴 Shashka", callback_data="checkers")],
        [InlineKeyboardButton("🏆 Reyting", callback_data="rating"),
         InlineKeyboardButton("📊 Statistika", callback_data="stats")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "♟️ Xush kelibsiz! O'yin tanlang:",
        reply_markup=reply_markup
    )

# Tugmalar bosilganda
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "chess":
        keyboard = [
            [InlineKeyboardButton("👥 Do'st bilan", callback_data="chess_friend")],
            [InlineKeyboardButton("🌐 Onlayn", callback_data="chess_online")],
            [InlineKeyboardButton("🤖 AI bilan", callback_data="chess_ai")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data="back")],
        ]
        await query.edit_message_text("♟️ Shahmat — rejim tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "checkers":
        keyboard = [
            [InlineKeyboardButton("👥 Do'st bilan", callback_data="checkers_friend")],
            [InlineKeyboardButton("🌐 Onlayn", callback_data="checkers_online")],
            [InlineKeyboardButton("🤖 AI bilan", callback_data="checkers_ai")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data="back")],
        ]
        await query.edit_message_text("🔴 Shashka — rejim tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("♟️ Shahmat", callback_data="chess"),
             InlineKeyboardButton("🔴 Shashka", callback_data="checkers")],
            [InlineKeyboardButton("🏆 Reyting", callback_data="rating"),
             InlineKeyboardButton("📊 Statistika", callback_data="stats")],
        ]
        await query.edit_message_text("♟️ Xush kelibsiz! O'yin tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))

    else:
        await query.edit_message_text(f"⏳ Bu bo'lim tez orada ishga tushadi!")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
