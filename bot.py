import os
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
from PIL import Image
import imagehash

TOKEN = "8618253311:AAESSUFWpVndRRqavHJMuXdNFMMwaAdYP0k"
IMAGE_FOLDER = "images"

# Start command
async def start(update, context):
    await update.message.reply_text(
        "🙏 Welcome!\n\n📸 Saree photo મોકલો અને Design Number મેળવો"
    )

# Photo handler
async def handle_photo(update, context):
    photo = update.message.photo[-1]
    file = await photo.get_file()

    user_path = "user.jpg"
    await file.download_to_drive(user_path)

    try:
        user_img = Image.open(user_path)
        user_hash = imagehash.average_hash(user_img)
    except:
        await update.message.reply_text("❌ Image read error")
        return

    best_match = None
    min_diff = 100

    for img_name in os.listdir(IMAGE_FOLDER):
        if img_name.lower().endswith((".jpg", ".jpeg", ".png")):
            try:
                img_path = os.path.join(IMAGE_FOLDER, img_name)
                db_img = Image.open(img_path)
                db_hash = imagehash.average_hash(db_img)

                diff = user_hash - db_hash

                if diff < min_diff:
                    min_diff = diff
                    best_match = img_name
            except:
                continue

    if best_match and min_diff < 5:
        design_no = best_match.split(".")[0]
        await update.message.reply_text(
            f"✨ Design Found!\n\n🧵 Design No: {design_no}\n\n📩 Order કરવા માટે contact કરો"
        )
    else:
        await update.message.reply_text(
            "❌ Design match નથી મળ્યો\n\n📸 Clear photo મોકલો"
        )

# App start
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("Bot Started...")
app.run_polling()