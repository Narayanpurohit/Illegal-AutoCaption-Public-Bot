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

start_message = """
<b>👋Hello {}</b>
<b>I am an AutoCaption bot</b>
<b>All you have to do is add me to your channel and I will show you my power</b>
<b>Maintained By : @Illegal_Developer</b>"""

about_message = """
<b>• Name : <a href=https://t.me/Illegal_Developer>AutoCaption</a></b>
<b>• Developer : <a href=https://t.me/Illegal_Developer>ɪʟʟᴇɢᴀʟ ᴅᴇᴠᴇʟᴏᴘᴇʀꜱ</a></b>
<b>• Language : Python3</b>
<b>• Library : Pyrogram v{version}</b>
<b>• Updates : <a href=https://t.me/Illegal_Developer>Click Here</a></b>"""

@AutoCaptionBotV1.on_message(pyrogram.filters.private & pyrogram.filters.command(["start"]))
def start_command(bot, update):
    update.reply(
        start_message.format(update.from_user.mention),
        reply_markup=start_buttons(bot, update),
        parse_mode=pyrogram.enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )

@AutoCaptionBotV1.on_callback_query(pyrogram.filters.regex("start"))
def strat_callback(bot, update):
    update.message.edit(
        start_message.format(update.from_user.mention),
        reply_markup=start_buttons(bot, update.message),
        parse_mode=pyrogram.enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )

@AutoCaptionBotV1.on_callback_query(pyrogram.filters.regex("about"))
def about_callback(bot, update):
    bot = bot.get_me()
    update.message.edit(
        about_message.format(
            version=pyrogram.__version__, username=bot.mention
        ),
        reply_markup=about_buttons(bot, update.message),
        parse_mode=pyrogram.enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )

@AutoCaptionBotV1.on_message(pyrogram.filters.channel)
def edit_caption(bot, update: pyrogram.types.Message):
    motech, _ = get_file_details(update)
    try:
        if motech:
            try:
                update.edit(custom_caption.format(file_name=motech.file_name))
            except pyrogram.errors.FloodWait as FloodWait:
                asyncio.sleep(FloodWait.value)
                update.edit(custom_caption.format(file_name=motech.file_name))
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
    if update.media:
        for message_type in (
            "photo",
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

def start_buttons(bot, update):
    bot = bot.get_me()
    buttons = [
        [
            pyrogram.types.InlineKeyboardButton(
                "Updates", url="https://t.me/Illegal_Developer"
            ),
            pyrogram.types.InlineKeyboardButton(
                "About 🤠", callback_data="about"
            ),
        ],
        [
            pyrogram.types.InlineKeyboardButton(
                "➕️ Add To Your Channel ➕️",
                url=f"http://t.me/{bot.username}?startchannel=true",
            )
        ],
    ]
    return pyrogram.types.InlineKeyboardMarkup(buttons)

def about_buttons(bot, update):
    buttons = [
        [
            pyrogram.types.InlineKeyboardButton(
                "🏠 Back To Home 🏠", callback_data="start"
            )
        ]
    ]
    return pyrogram.types.InlineKeyboardMarkup(buttons)

print("Telegram AutoCaption")
