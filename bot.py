import os             # <--- এই লাইনটি অবশ্যই যোগ করো
import sys
import subprocess
import shutil
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Render এর এনভায়রনমেন্ট ভেরিয়েবল থেকে টোকেন নেওয়া হচ্ছে
TOKEN = os.environ.get('BOT_TOKEN') 


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is now ACTIVE! Send me an APK and I'll process it.")

async def handle_apk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    chat_id = update.message.chat_id
    input_apk = f"input_{chat_id}.apk"
    output_apk = f"modded_{chat_id}.apk"
    
    await file.download_to_drive(input_apk)
    await update.message.reply_text("⚙️ Processing... Please wait.")

    try:
        # Apktool process
        subprocess.run(['apktool', 'd', input_apk, '-o', 'decompiled_folder'], check=True)
        subprocess.run(['apktool', 'b', 'decompiled_folder', '-o', output_apk], check=True)
        
        # Signing process
        subprocess.run(['java', '-jar', '/uber-apk-signer.jar', '--apks', output_apk], check=True)

        # Sending the file
        with open(f"{output_apk}-aligned-signed.apk", 'rb') as f:
            await update.message.reply_document(f, caption="✅ Here is your bypassed APK!")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
    
    finally:
        # Cleanup
        if os.path.exists(input_apk): os.remove(input_apk)
        if os.path.exists(output_apk): os.remove(output_apk)
        if os.path.exists('decompiled_folder'): shutil.rmtree('decompiled_folder')

if __name__ == "__main__":
    if not TOKEN:
        print("Error: BOT_TOKEN not found in environment variables!")
    else:
        print("Bot is starting...")
        app = Application.builder().token(TOKEN).build()
        app.add_handler(MessageHandler(filters.Document.APK, handle_apk))
        # Start command support
        from telegram.ext import CommandHandler
        app.add_handler(CommandHandler("start", start))
        app.run_polling()
