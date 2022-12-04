import os
import re
import requests
import mimetypes
from urllib.parse import unquote_plus
from telegram import InlineKeyboardMarkup
from telegram.ext import CommandHandler
from subprocess import run
from bot import dispatcher
from bot.helper.telegram_helper import button_builders
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.bot_utils import get_readable_file_size
from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage, sendMarkup
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.ext_utils.telegraph_helper import telegraph


def extract_mediainfo(link: str, bot, update):
    __response = requests.head(link, stream=True)
    msg = sendMessage("Getting MediaInfo ...", bot, update.message)
    try:
        file_size = get_readable_file_size(int(__response.headers["Content-Length"].strip()))
        file_name = unquote_plus(link).rsplit('/', 1)[-1]
        mime_type = __response.headers.get("Content-Type", mimetypes.guess_type(file_name)).rsplit(";", 1)[0]
        result = run(f'mediainfo "{link}"', capture_output=True, shell=True)
        stderr = result.stderr.decode('utf-8')
        stdout = result.stdout.decode('utf-8')
        metadata = re.sub(
            rf"http(s)?://.*\.{link.rsplit('.', 1)[-1]}",
            file_name, stdout.replace("\r", "")
        )
        html = "<h3>Metadata of {}</h3>" \
               "<br><br>" \
               "<pre>{}</pre>"
        page = telegraph.create_page(
            title="Mediainfo by Mayur",
            content=html.format(file_name, metadata)
        )
        button = button_builders.ButtonMaker()
        button.build_button("MediaInfo", page['url'])
        reply_markup = InlineKeyboardMarkup(button.build_menu(1))
        deleteMessage(bot, msg)
        sendMarkup(
            f"<b>File Name:</b> <code>{file_name}</code>\n"
            f"<b>File Size:</b> <code>{file_size}</code>\n"
            f"<b>Type:</b> <code>{mime_type}</code>\n",
            bot, update.message, reply_markup
        )
    except KeyError:
        deleteMessage(bot, msg)
        sendMessage("<b>Not a valid direct downloadable video!</b>", bot, update.message)
    except Exception as err:
        deleteMessage(bot, msg)
        sendMessage(f"<b>Error:</b> <code>{err}</code>", bot, update.message)


def mediainfo_cmd_handler(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) > 1:
        link = args[1]
    else:
        return sendMessage(f"Send a streamable link along with command", context.bot, update.message)
    extract_mediainfo(link, context.bot, update)


mi_cmd_handler = CommandHandler(
    BotCommands.MInfoCommand,
    mediainfo_cmd_handler,
    filters=CustomFilters.authorized_chat | CustomFilters.authorized_user,
    run_async=True
)
dispatcher.add_handler(mi_cmd_handler)
