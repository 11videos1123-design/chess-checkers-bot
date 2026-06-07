import os
import chess
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Faol o'yinlar
games = {}

def board_to_text(board):
    pieces = {
        'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
        'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚',
    }
    rows = []
    for rank in range(7, -1, -1):
        row = f"{rank+1} "
        for file in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            if piece:
                row += pieces.get(piece.symbol(), '?')
            else:
                row += '⬜' if (rank + file) % 2 == 0 else '⬛'
        rows.append(row)
    rows.append("  abcdefgh")
    return "\n".join(rows)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("♟️ Shahmat", callback_data="chess"),
         InlineKeyboardButton("🔴 Shashka", callback_data="checkers")],
        [InlineKeyboardButton("🏆 Reyting", callback_data="rating"),
         InlineKeyboardButton("📊 Statistika", callback_data="stats")],
    ]
    await update.message.reply_text(
        "♟️ Xush kelibsiz! O'yin tanlang:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "chess":
        keyboard = [
            [InlineKeyboardButton("🤖 AI bilan o'ynash", callback_data="chess_ai")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data="back")],
        ]
        await query.edit_message_text("♟️ Shahmat — rejim tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "chess_ai":
        board = chess.Board()
        games[user_id] = {"board": board, "mode": "ai"}
        text = board_to_text(board)
        keyboard = [[InlineKeyboardButton("❌ O'yinni tugatish", callback_data="end_game")]]
        await query.edit_message_text(
            f"♟️ Shahmat boshlandi! Siz oq tomonsiz.\n\n{text}\n\nYurishingizni yozing (masalan: e2e4)",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "end_game":
        if user_id in games:
            del games[user_id]
        await query.edit_message_text("O'yin tugadi! /start dan qayta boshlang.")

    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("♟️ Shahmat", callback_data="chess"),
             InlineKeyboardButton("🔴 Shashka", callback_data="checkers")],
            [InlineKeyboardButton("🏆 Reyting", callback_data="rating"),
             InlineKeyboardButton("📊 Statistika", callback_data="stats")],
        ]
        await query.edit_message_text("♟️ Xush kelibsiz! O'yin tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))

    else:
        await query.edit_message_text("⏳ Bu bo'lim tez orada ishga tushadi!")

async def move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in games:
        await update.message.reply_text("O'yin yo'q! /start dan boshlang.")
        return

    game = games[user_id]
    board = game["board"]
    user_move = update.message.text.strip()

    try:
        chess_move = chess.Move.from_uci(user_move)
        if chess_move in board.legal_moves:
            board.push(chess_move)

            if board.is_checkmate():
                await update.message.reply_text(f"{board_to_text(board)}\n\n🎉 Siz yutdingiz!")
                del games[user_id]
                return

            # AI yurishi (oddiy — birinchi legal yurish)
            ai_move = list(board.legal_moves)[0]
            board.push(ai_move)

            if board.is_checkmate():
                await update.message.reply_text(f"{board_to_text(board)}\n\n🤖 AI yutdi!")
                del games[user_id]
                return

            keyboard = [[InlineKeyboardButton("❌ O'yinni tugatish", callback_data="end_game")]]
            await update.message.reply_text(
                f"{board_to_text(board)}\n\n🤖 AI yurishi: {ai_move}\nSizning navbatingiz:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update.message.reply_text("❌ Noto'g'ri yurish! Qaytadan yozing (masalan: e2e4)")
    except:
        await update.message.reply_text("❌ Format noto'g'ri! Shunday yozing: e2e4")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, move))
    app.run_polling()

if __name__ == "__main__":
    main()
