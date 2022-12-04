import re
import random
import string

from telegram.ext import CommandHandler

from bot import LOGGER, dispatcher, CLONE_LIMIT, download_dict, download_dict_lock, Interval
from bot.helper.mirror_utils.upload_utils.gdriveToolss import GoogleDriveHelper
from bot.helper.ext_utils.bot_utilss import new_thread, get_readable_file_size, is_gdrive_link, \
    is_appdrive_link, is_gdtot_link, is_hubdrive_link, is_sharer_link
from bot.helper.ext_utils.clone_status import CloneStatus
from bot.helper.ext_utils.exceptionss import ExceptionHandler
from bot.helper.ext_utils.parser import appdrive, gdtot, HubDrive, sharer
from bot.helper.telegram_helper.message_utilss import sendMessage, editMessage, deleteMessage, \
    delete_all_messages, update_all_messages, sendStatusMessage
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters

@new_thread
def clonesNode(update, context):
    LOGGER.info(f"User: {update.message.from_user.first_name} [{update.message.from_user.id}]")
    args = update.message.text.split(" ", maxsplit=2)
    reply_to = update.message.reply_to_message
    link = ''
    key = ''
    if len(args) > 1:
        link = args[1]
        try:
            key = args[2]
        except IndexError:
            pass
    if reply_to is not None:
        link = reply_to.text
        if len(args) > 1:
            key = args[1]
    links = re.findall(r'(https?://\S+)', link)
    results = ""
    for link in links:
        is_appdrive = is_appdrive_link(link)
        is_gdtot = is_gdtot_link(link)
        is_hubdrive = is_hubdrive_link(link)
        is_sharer = is_sharer_link(link)
        if (is_appdrive or is_gdtot or is_hubdrive or is_sharer):
            msg = sendMessage(f"Processing: <code>{link}</code>", context.bot, update.message)
            LOGGER.info(f"Processing: {link}")
            try:
                if is_appdrive:
                    appdict = appdrive(link)
                    link = appdict.get('gdrive_link')
                if is_gdtot:
                    link = gdtot(link)
                if is_hubdrive:
                    link = HubDrive().hubdrive_dl(link)
                if is_sharer:
                    link = sharer(link)
                deleteMessage(context.bot, msg)
            except ExceptionHandler as e:
                deleteMessage(context.bot, msg)
                LOGGER.error(e)
                sendMessage(str(e), context.bot, update.message)
                continue
        if is_gdrive_link(link):
            msg = sendMessage(f"Checking: <code>{link}</code>", context.bot, update.message)
            gd = GoogleDriveHelper()
            res, size, name, files = gd.helper(link)
            deleteMessage(context.bot, msg)
            if res != "":
                sendMessage(res, context.bot, update.message)
                continue
            if CLONE_LIMIT is not None:
                if size > CLONE_LIMIT * 1024**3:
                    msg2 = f"<b>Name:</b> <code>{name}</code>"
                    msg2 += f"\n<b>Size:</b> {get_readable_file_size(size)}"
                    msg2 += f"\n<b>Limit:</b> {CLONE_LIMIT} GiB"
                    msg2 += "\n\n<b>⚠️ Task failed</b>"
                    sendMessage(msg2, context.bot, update.message)
                    continue
            if files <= 20:
                msg = sendMessage(f"Cloning: <code>{link}</code>", context.bot, update.message)
                LOGGER.info(f"Cloning: {link}")
                result = gd.clone(link, key)
                deleteMessage(context.bot, msg)
            else:
                drive = GoogleDriveHelper(name)
                gid = ''.join(random.SystemRandom().choices(string.ascii_letters + string.digits, k=12))
                clone_status = CloneStatus(drive, size, files, update.message, gid)
                with download_dict_lock:
                    download_dict[update.message.message_id] = clone_status
                sendStatusMessage(update.message, context.bot)
                LOGGER.info(f"Cloning: {link}")
                result = drive.clone(link, key)
                with download_dict_lock:
                    del download_dict[update.message.message_id]
                    count = len(download_dict)
                try:
                    if count == 0:
                        Interval[0].cancel()
                        del Interval[0]
                        delete_all_messages()
                    else:
                        update_all_messages()
                except IndexError:
                    pass
            results += result + "\n\n"
            if is_gdtot:
                LOGGER.info(f"Deleting: {link}")
                gd.deleteFile(link)
            elif is_appdrive:
                if appdict.get('link_type') == 'login':
                    LOGGER.info(f"Deleting: {link}")
                    gd.deleteFile(link)
        elif "Your Google Drive storage is full" in link:
            sendMessage(link, context.bot, update.message)
        elif "File was not Found" in link:
            sendMessage(link, context.bot, update.message)
        else:
            sendMessage("Send a Google Drive, AppDrive, DriveApp, GDToT, Sharer, HubDrive, DriveHub, KatDrive, Kolop, DriveLinks link along with command", context.bot, update.message)
            LOGGER.info("Cloning: None")
    sendMessage(results, context.bot, update.message)

clones_handler = CommandHandler(BotCommands.ClonesCommand, clonesNode,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(clones_handler)
