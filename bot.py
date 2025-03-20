import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import csv
import sqlite3
import io
from datetime import datetime

# ডাটাবেস সেটআপ
conn = sqlite3.connect('posts.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS posts
             (id INTEGER PRIMARY KEY AUTOINCREMENT, post_text TEXT, date TEXT)''')
conn.commit()

# লগিং কনফিগারেশন
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('🎉 হ্যালো! আমাকে যেকোনো টেক্সট পাঠান, আমি সেটি সেভ করব। /getcsv কমান্ড দিয়ে CSV ফাইল পাবেন।')

def save_post(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    post_text = update.message.text
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute("INSERT INTO posts (post_text, date) VALUES (?, ?)", (post_text, timestamp))
    conn.commit()
    logger.info(f"New post from {user.first_name}: {post_text[:50]}...")
    update.message.reply_text("✅ পোস্ট সেভ করা হয়েছে!")

def generate_csv(update: Update, context: CallbackContext) -> None:
    csv_file = io.BytesIO()
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['ID', 'পোস্ট', 'তারিখ'])
    
    c.execute("SELECT * FROM posts")
    for row in c.fetchall():
        csv_writer.writerow(row)
    
    csv_file.seek(0)
    csv_file.name = 'সকল_পোস্ট.csv'
    update.message.reply_document(document=csv_file, caption="📁 আপনার সংগ্রহ করা পোস্টগুলো:")

def main() -> None:
    # টোকেন এখানে বসান (এনভায়রনমেন্ট ভেরিয়েবল ব্যবহার করা ভালো)
    TOKEN = "7882898983:AAETpNJpJPTKy8NVnMf0Opnrzy779eJDOkQ"
    updater = Updater(7882898983:AAETpNJpJPTKy8NVnMf0Opnrzy779eJDOkQ)
    dispatcher = updater.dispatcher

    # কমান্ড হ্যান্ডলার
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("getcsv", generate_csv))

    # মেসেজ হ্যান্ডলার
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, save_post))

    # বট শুরু করুন
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()