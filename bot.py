import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# হেলথ চেক হ্যান্ডলার (Render-এর জন্য প্রয়োজনীয়)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is alive and running!")

def run_health_server():
    port = int(os.environ.get("PORT", 10000)) # ডাইনামিক পোর্ট ব্যবহার
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

TOKEN = os.environ.get('BOT_TOKEN')

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is ACTIVE! Send me an APK.")

async def handle_apk(update, context: ContextTypes.DEFAULT_TYPE):
    # এখানে আপনার APK প্রসেসিং কোড লিখুন
    await update.message.reply_text("APK received! Processing...")

if __name__ == "__main__":
    if not TOKEN:
        print("Error: BOT_TOKEN not found!")
        exit(1)

    # হেলথ সার্ভারটি আলাদা থ্রেডে চলবে যাতে Render মনে করে অ্যাপটি লাইভ আছে
    threading.Thread(target=run_health_server, daemon=True).start()

    application = Application.builder().token(TOKEN).build()
    
    # কমান্ড হ্যান্ডলার এবং ডকুমেন্ট হ্যান্ডলার যোগ করুন
    from telegram.ext import CommandHandler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_apk))

    print("Bot is starting...")
    application.run_polling()
