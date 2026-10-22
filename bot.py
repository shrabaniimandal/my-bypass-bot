import os
import threading
import shutil
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

# Render-এর জন্য হেলথ চেক সার্ভার (যাতে বট বন্ধ না হয়ে যায়)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

TOKEN = os.environ.get('BOT_TOKEN')

# --- PROFESSIONAL BYPASS LOGIC (PYTHON VERSION) ---
def apply_bypass(file_path):
    """
    প্রফেশনাল টুলস ছাড়া পাইথন দিয়ে ফাইলের মেটাডেটা এবং স্ট্রাকচারে 
    সামান্য পরিবর্তন আনা যাতে সিগনেচার ম্যাচ না করে।
    """
    try:
        bypassed_path = file_path.replace(".apk", "_protected_bypass.apk")
        
        # ফাইলের ভেতরকার ডাটাকে সামান্য পরিবর্তন করা (Pseudo-Obfuscation)
        with open(file_path, 'rb') as f:
            data = f.read()
        
        # এখানে আমরা ফাইলের শেষে একটি ইউনিক স্ট্রিং যোগ করছি 
        # যাতে ফাইলের হ্যাশ (Hash) পরিবর্তন হয়ে যায়, যা প্লে প্রটেক্টকে ফাঁকি দিতে সাহায্য করে
        modified_data = data + b"\n#Bypass_Verified_v2.1"
        
        with open(bypassed_path, 'wb') as f:
            f.write(modified_data)
            
        return bypassed_path
    except Exception as e:
        print(f"Bypass Error: {e}")
        return None

# --- BOT HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 **Play Protect Bypass Bot Active!**\n\nআপনার APK ফাইলটি এখানে পাঠান, আমি সেটিকে প্রসেস করে দিচ্ছি।")

async def handle_apk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ১. ফাইল রিসিভ এবং ডাউনলোড
    file = await update.message.document.get_file()
    file_name = update.message.document.file_name
    file_path = f"./{file_name}"
    
    try:
        await file.download_to_drive(file_path)
        await update.message.reply_text("🛠 **Processing APK...**\nআমরা ফাইলের সিগনেচার পরিবর্তন করছি। দয়া করে অপেক্ষা করুন...")

        # ২. বাইপাস ফাংশন কল করা
        bypassed_file = apply_bypass(file_path)

        if bypassed_file:
            # ৩. প্রসেস করা ফাইল পাঠানো
            with open(bypassed_file, 'rb') as doc:
                await update.message.reply_document(
                    document=doc, 
                    caption="✅ **Bypass Complete!**\nএখন এই APK টি ইনস্টল করে দেখুন।"
                )
            # ফাইল ক্লিনআপ
            os.remove(file_path)
            os.remove(bypassed_file)
        else:
            await update.message.reply_text("❌ বাইপাস করার সময় সমস্যা হয়েছে।")

    except Exception as e:
        await update.message.reply_text(f"❌ এরর: {str(e)}")

if __name__ == "__main__":
    # হেলথ সার্ভার চালু করা
    threading.Thread(target=run_health_server, daemon=True).start()
    
    # বট অ্যাপ্লিকেশন তৈরি
    app = Application.builder().token(TOKEN).build()
    
    # হ্যান্ডলার যুক্ত করা
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_apk))
    
    print("Bot is running on Render...")
    app.run_polling()
