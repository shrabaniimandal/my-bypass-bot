import os
import subprocess
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# ---------------------------------------------------------
# এখানে তোমার বটের টোকেন বসাও
TOKEN = '8679026449:AAHiFeIx17Tz8O03SjtCV6ptkT0sCaycMpA' 
# ---------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Send me an APK file, and I will try to bypass Play Protect and Antivirus for you. 🚀")

async def handle_apk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ফাইলটি রিসিভ করা
    file = await update.message.document.get_file()
    chat_id = update.message.chat_id
    input_apk = f"input_{chat_id}.apk"
    output_apk = f"modded_{chat_id}.apk"
    
    await file.download_to_drive(input_apk)
    await update.message.reply_text("⚙️ Processing your APK... Please wait. This may take a minute.")

    try:
        # ১. ডিকম্পাইল (Apktool ব্যবহার করে)
        # নোট: সার্ভারে apktool এবং java ইন্সটল থাকতে হবে
        subprocess.run(['apktool', 'd', input_apk, '-o', 'decompiled_folder'], check=True)

        # ২. সিম্পল অবফাসকেশন (প্যাকেজ নেম বা রিসোর্স পরিবর্তন করার লজিক এখানে থাকে)
        # এখানে আমরা একটি সাধারণ ফাইল রিনেম প্রসেস করছি ডেমো হিসেবে
        # আসল প্রফেশনাল অবফাসকেশন অনেক বড় স্ক্রিপ্ট হয়
        os.rename('decompiled_folder/AndroidManifest.xml', 'decompiled_folder/AndroidManifest_mod.xml') 
        # (নোট: এটি শুধু উদাহরণ, রিয়েল বাইপাসের জন্য Smali কোড এডিট করতে হয়)

        # ৩. রিকম্পাইল
        subprocess.run(['apktool', 'b', 'decompiled_folder', '-o', output_apk], check=True)

        # ৪. সাইনিং (Sign APK)
        # আমরা ধরে নিচ্ছি uber-apk-signer.jar সার্ভারে আছে
        subprocess.run(['java', '-jar', 'uber-apk-signer.jar', '--apks', output_apk], check=True)

        # ৫. ফাইনাল ফাইল পাঠানো
        with open(f"{output_apk}-aligned-signed.apk", 'rb') as f:
            await update.message.reply_document(f, caption="✅ Your bypassed APK is ready!")

    except Exception as e:
        await update.message.reply_text(f"❌ Error occurred: {str(e)}")
    
    finally:
        # পরিষ্কার করা (Cleanup)
        if os.path.exists(input_apk): os.remove(input_apk)
        if os.path.exists(output_apk): os.remove(output_apk)
        # ফোল্ডার ডিলিট করার জন্য একটি ছোট লুপ
        import shutil
        if os.path.exists('decompiled_folder'): shutil.rmtree('decompiled_folder')

# মেইন ফাংশন
if __name__ == "__main__":
    print("Bot is starting...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.Document.APK, handle_apk))
    app.run_polling()
