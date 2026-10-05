
import os
import logging
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ==================== BOT TOKEN ====================
TELEGRAM_BOT_TOKEN = "8859694055:AAGDubA7r050uZq5U_0ZYNlaN_Oov4dQUNc"
# ===================================================

# Loglarni sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ----------------- UNICODE SHRIFT MAPPINGLARI -----------------
# 1-uslub: Small Caps (ᴍᴀꜱᴛᴇʀᴍɪɴᴅ)
SMALL_CAPS_MAP = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ0123456789"
)

# 2-uslub: Bold Italic Serif (𝑴𝑴𝑫 / 𝑩𝒊𝒃𝒊)
BOLD_ITALIC_MAP = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "𝒂𝒃𝒄𝒅ｅ𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎ｎ𝒐\\𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁"
)

def generate_nicks(name: str) -> tuple[str, str]:
    """Ismni 2 xil jamoaviy uslubga o'girish funksiyasi."""
    clean_name = name.strip()
    
    # 1-uslub: 🎩 ᴍᴀꜱᴛᴇʀᴍɪɴᴅ 🎩 • ᴅᴏʙʀɪʏ ©
    style1_name = clean_name.translate(SMALL_CAPS_MAP)
    nick1 = f"🎩 ᴍᴀꜱᴛᴇʀᴍɪɴᴅ 🎩 • {style1_name} ©"
    
    # 2-uslub: 🎩 𝑴𝑴𝑫 ™ 𝑩𝒊𝒃𝒊 🎩 ©
    style2_name = clean_name.translate(BOLD_ITALIC_MAP)
    nick2 = f"🎩 𝑴𝑴𝑫 ™ {style2_name} 🎩 ©"
    
    return nick1, nick2

# ----------------- FLASK WEBSERVER (24/7 XOSTING UCHUN) -----------------
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot muvaffaqiyatli ishlamoqda!", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app_flask.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# ----------------- TELEGRAM BOT BUYRUKLARI -----------------
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "<b>Salom! Men jamoaviy nik yaratuvchi botman.</b> 🎩\n\n"
        "Botdan foydalanish uchun guruhda yoki shaxsiyda quyidagi buyruqni yuboring:\n\n"
        "• <code>/nik Dobriy</code>\n"
        "• <code>/nick Bibi</code>\n\n"
        "<i>Agar ism yozmasangiz, Telegram'dagi ismingizdan foydalaniladi.</i>"
    )
    if update.message:
        await update.message.reply_html(welcome_text)

async def nick_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
        
    user = update.effective_user
    
    # Agar argument berilgan bo'lsa o'shani oladi, bo'lmasa foydalanuvchining ismini
    if context.args:
        target_name = " ".join(context.args)
    elif user and user.first_name:
        target_name = user.first_name
    else:
        target_name = "User"

    # 2 xil nikni tayyorlash
    nick1, nick2 = generate_nicks(target_name)
    
    reply_text = (
        f"<b>{target_name}</b> uchun jamoaviy niklar:\n\n"
        f"<b>1-uslub:</b>\n<code>{nick1}</code>\n\n"
        f"<b>2-uslub:</b>\n<code>{nick2}</code>\n\n"
        f"<i>(Nusxalash uchun nik ustiga bir marta bosing)</i>"
    )
    
    await update.message.reply_html(reply_text)

# ----------------- MAIN ISHGA TUSHIRISH -----------------
if __name__ == '__main__':
    # Flask veb-serverini fonda yurgizish
    keep_alive()
    
    # Telegram botni sozlash va yurgizish
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler(["nik", "nick"], nick_command))
    
    print(">>> Bot muvaffaqiyatli ishga tushdi! <<<")
    app.run_polling(drop_pending_updates=True)

Buni bot.py fayli ichiga joylab, saqlang.
