import os
import sys
import subprocess
import shutil
import threading # <--- এটি যোগ করো
from http.server import HTTPServer, BaseHTTPRequestHandler # <--- এটি যোগ করো
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# ১. Render-এর জন্য একটি ছোট্ট হেলথ-চেক সার্ভার (যাতে ফ্রি-তে চলে)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive and running!")

def run_health_server():
    # Render সাধারণত ১০০০০ পোর্ট ব্যবহার করে
    server = HTTPServer(('0.0.0.0', 10000), HealthCheckHandler)
    server.serve_forever()

# --- বাকি সব কোড তোমার আগের মতোই থাকবে ---
TOKEN = os.environ.get('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot is ACTIVE! Send me an APK.")

async def handle_apk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ... (তোমার আগের handle_apk ফাংশনটি এখানে থাকবে) ...
    # আমি সংক্ষেপ করছি, তোমার আগের handle_apk কোডটিই রেখো।
    pass 

if __name__ == "__main__":
    if not TOKEN:
        print("Error: BOT_TOKEN not found!")
        sys.exit(1)
    
    # ২. এই লাইনটি যোগ করো: এটি আলাদা থ্রেডে সার্ভার চালাবে যাতে Render খুশি থাকে
    threading.Thread(target=run_health_server, daemon=True).start()
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.Document.APK, handle_apk))
    print("Bot is starting and Health Server is active on port 10000...")
    app.run_polling()
