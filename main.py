import io
import os
import aiofiles

from PIL import Image

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import filters, CommandHandler, MessageHandler, CallbackContext, ApplicationBuilder

from dotenv import load_dotenv

from gemini_api import handle_gemini_model, handle_gemini_image
from helpers import format_text_to_html
from messages import WELCOME_MESSAGE, HELP_MESSAGE
from notion_api import add_notion_page
from openai_api import handle_transcribe_openai

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

model_name = ["gemini", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"]


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(WELCOME_MESSAGE, parse_mode=ParseMode.HTML)


async def send_help(update: Update, context: CallbackContext):
    await update.message.reply_text(HELP_MESSAGE, parse_mode=ParseMode.HTML)


async def handle_image(update: Update, context: CallbackContext):
    placeholder_message = await update.message.reply_text("...")
    await update.message.chat.send_action(action="typing")
    chat_id = update.message.chat_id
    image_file = await context.bot.getFile(update.message.photo[-1].file_id)
    image_data = await image_file.download_as_bytearray()

    async with aiofiles.open('temp.png', 'wb') as out_file:
        await out_file.write(image_data)

    img = Image.open('temp.png')
    result = handle_gemini_image(img)
    reply = add_notion_page(result)
    await context.bot.edit_message_text(reply, chat_id=placeholder_message.chat_id,
                                        message_id=placeholder_message.message_id)


async def handle_voice(update: Update, context: CallbackContext):
    placeholder_message = await update.message.reply_text("...")
    await update.message.chat.send_action(action="typing")
    voice = update.message.voice
    voice_file = await context.bot.get_file(voice.file_id)

    buf = io.BytesIO()
    await voice_file.download_to_memory(buf)
    buf.name = "voice.oga"  # file extension is required
    buf.seek(0)  # move cursor to the beginning of the buffer
    result = handle_transcribe_openai(buf)
    reply = add_notion_page(result)
    await context.bot.edit_message_text(reply, chat_id=placeholder_message.chat_id,
                                        message_id=placeholder_message.message_id)

async def echo(update: Update, context: CallbackContext):

    placeholder_message = await update.message.reply_text("...")
    await update.message.chat.send_action(action="typing")

    chat_id = update.message.chat.id
    input_text = update.message.text

    try:
        bot_reply = add_notion_page(input_text)
        html_text = format_text_to_html(bot_reply)
        await context.bot.edit_message_text(html_text, chat_id=placeholder_message.chat_id,
                                            message_id=placeholder_message.message_id,
                                            parse_mode=ParseMode.HTML)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', send_help)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    photo_handler = MessageHandler(filters.PHOTO, handle_image)
    voice_handler = MessageHandler(filters.VOICE, handle_voice)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(message_handler)
    application.add_handler(photo_handler)
    application.add_handler(voice_handler)

    application.run_polling()
