from dotenv import load_dotenv
import json
import os
import random
from telegram import InputFile
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def load_approved_users():
    # Fungsi ini akan mencoba membuka file approved_users.json
    # Jika file tidak ditemukan, akan mengembalikan set kosong
    # Jika file ditemukan, akan membaca data dari file dan mengembalikan set pengguna yang telah disetujui
    approved_users = set()
    try:
        with open("approved_users.json", "r") as f:
            data = json.load(f)
            if "approved_users" in data:
                approved_users = set(data["approved_users"])
    except FileNotFoundError:
        pass
    return approved_users


def save_approved_users(approved_users):
    # Fungsi ini akan menyimpan data set approved_users ke dalam file approved_users.json
    data = {"approved_users": list(approved_users)}
    with open("approved_users.json", "w") as f:
        json.dump(data, f)

# Initialize bot
bot = Bot(BOT_TOKEN)

# Variabel set approved_users akan diinisialisasi dengan set pengguna yang telah disetujui
approved_users = load_approved_users()

# Handler untuk command /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hai! Untuk bergabung pada FWB Distrik, silakan kirimkan pesan.")

# Handler untuk command /id
def get_id(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    update.message.reply_text(f"ID Anda adalah: {user_id}")

# Handler untuk command /approve
def approve(update: Update, context: CallbackContext):
    if update.message.from_user.id == int(PEMILIK_BOT_ID):
        try:
            user_id = int(context.args[0])
            approved_users.add(user_id)
            save_approved_users(approved_users)
            update.message.reply_text(f"User dengan ID {user_id} berhasil disetujui untuk mengirim pesan ke channel.")
        except (IndexError, ValueError):
            update.message.reply_text("Format command salah. Gunakan /approve <user_id>")
    else:
        update.message.reply_text("Anda tidak diizinkan untuk melakukan approve.")

# Handler untuk pesan
def message_handler(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    message_text = update.message.text
    
    if user_id in approved_users:
        # Cek apakah pesan memiliki hashtag #fwbboy atau #fwbgirl
        if "#fwbboy" in message_text:
            photos_dir = './public/boy/'
            photo_files = os.listdir(photos_dir)
            photo_file = random.choice(photo_files)
            with open(photos_dir + photo_file, 'rb') as photo:
                bot.send_photo(chat_id="@fwbchanneI", photo=InputFile(photo), caption=message_text)
        elif "#fwbgirl" in message_text:
            photos_dir = './public/girl/'
            photo_files = os.listdir(photos_dir)
            photo_file = random.choice(photo_files)
            with open(photos_dir + photo_file, 'rb') as photo:
                bot.send_photo(chat_id="@fwbchanneI", photo=InputFile(photo), caption=message_text)
        else:
            bot.send_message(chat_id="@fwbchanneI", text=message_text)
    
    

    else:
        # jika belum, beri notifikasi
        update.message.reply_text("Anda belum bergabung pada FWB Channel. Silakan hubungi admin untuk informasi lebih lanjut.")

# buat updater dan jadwalkan polling 
updater = Updater(BOT_TOKEN, use_context=True)

dispatcher = updater.dispatcher
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("approve", approve))
updater.dispatcher.add_handler(CommandHandler("id", get_id))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))
updater.start_polling()
updater.idle()
