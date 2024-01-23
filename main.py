import pyrogram
import os
import asyncio
import re

try:
    app_id = int(os.environ.get("app_id", "123456"))
except Exception as app_id:
    print(f"⚠️ App ID Invalid {app_id}")

try:
    api_hash = os.environ.get("api_hash", "71e4d726e727190eaa8c0486f0d")
except Exception as api_id:
    print(f"⚠️ Api Hash Invalid {api_hash}")

try:
    bot_token = os.environ.get("bot_token", "6631918034:AAFzEUUyh_PrrgIttLdtr_")
except Exception as bot_token:
    print(f"⚠️ Bot Token Invalid {bot_token}")

try:
    custom_caption = os.environ.get("custom_caption", """ 
<b>{file_name} ~ @missqueenbotx</b>""")
except Exception as custom_caption:
    print(f"⚠️ Custom Caption Invalid {custom_caption}")

AutoCaptionBotV1 = pyrogram.Client(
    name="AutoCaptionBotV1", api_id=app_id, api_hash=api_hash, bot_token=bot_token
)

@AutoCaptionBotV1.on_message(pyrogram.filters.private & pyrogram.filters.command(["start"]))
def start_command(bot, update):
    update.reply(
        "👋 Hello! I'm your AutoCaption bot.",
        parse_mode=pyrogram.enums.ParseMode.HTML,
    )

@AutoCaptionBotV1.on_message(pyrogram.filters.channel)
def edit_caption(bot, update: pyrogram.types.Message):
    motech, file_id = get_file_details(update)
    try:
        if motech:
            try:
                update.edit(custom_caption.format(file_name=file_id))
            except pyrogram.errors.FloodWait as FloodWait:
                asyncio.sleep(FloodWait.value)
                update.edit(custom_caption.format(file_name=file_id))
    except pyrogram.errors.MessageNotModified:
        pass

@AutoCaptionBotV1.on_message(pyrogram.filters.private)
def handle_custom_message(bot, update):
    try:
        chat_id = update.chat.id
        user_message = update.text

        # Define the pattern for the message
        pattern = re.compile(r'https://m\.easysky\.in/([A-Za-z0-9]+)')

        # Find all matches in the message
        matches = re.findall(pattern, user_message)

        # Replace matches with the desired URL
        updated_message = user_message
        for match in matches:
            updated_message = updated_message.replace(
                f'https://m.easysky.in/{match}', f'https://techy.veganab.co//{match}'
            )

        # Send the updated message back to the user
        bot.send_message(chat_id, updated_message, parse_mode=pyrogram.enums.ParseMode.HTML)
    except Exception as e:
        bot.send_message(chat_id, f"Error during find and replace: {str(e)}")

def get_file_details(update: pyrogram.types.Message):
    if update.photo:
        # If it's a photo, use the file_id as the unique identifier
        return update.photo, update.photo.file_id

    for message_type in (
        "animation",
        "audio",
        "document",
        "video",
        "video_note",
        "voice",
        "sticker",
    ):
        obj = getattr(update, message_type, None)
        if obj:
            return obj, obj.file_id

    return None, None

print("Telegram AutoCaption Bot Start")

if __name__ == "__main__":
    AutoCaptionBotV1.run()
