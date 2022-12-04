import re
import shlex
from subprocess import Popen, PIPE
from telegram.ext import CommandHandler

from bot import LOGGER, dispatcher
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage

def ffmpeg(update, context):
    message = update.effective_message
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) == 1:
        cmd = f"ffmpeg"
    if len(args) > 1:
        link = args[1]
        cmd = f"ffmpeg {link}"
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if len(stdout) != 0:
        reply += f"{stdout}\n"
        LOGGER.info(f"Ffmpeg - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"{stderr}\n"
        LOGGER.error(f"Ffmpeg - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('ffmpeg_output.txt', 'w') as file:
            file.write(reply)
        with open('ffmpeg_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    elif len(reply) != 0:
        message.reply_text(reply, parse_mode='Markdown')
    else:
        message.reply_text('No Reply', parse_mode='Markdown')

def mkvmerge(update, context):
    message = update.effective_message
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) == 1:
        cmd = f"mkvmerge"
    if len(args) > 1:
        link = args[1]
        cmd = f"mkvmerge {link}"
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if len(stdout) != 0:
        reply += f"{stdout}\n"
        LOGGER.info(f"Mkvmerge - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"{stderr}\n"
        LOGGER.error(f"Mkvmerge - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('mkvmerge_output.txt', 'w') as file:
            file.write(reply)
        with open('mkvmerge_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    elif len(reply) != 0:
        message.reply_text(reply, parse_mode='Markdown')
    else:
        message.reply_text('No Reply', parse_mode='Markdown')

def mediainfo(update, context):
    message = update.effective_message
    args = update.message.text.split(" ", maxsplit=1)
    link = 'mediainfo'
    if len(args) == 1:
        cmd = f""
    if len(args) > 1:
        link = args[1]
        cmd = f"mediainfo {link}"
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if len(stdout) != 0:
        reply += f"{stdout}\n"
        LOGGER.info(f"Mediainfo - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"{stderr}\n"
        LOGGER.error(f"Mediainfo - {cmd} - {stderr}")
    if len(reply) > 1500:
        with open('mediainfo_output.txt', 'w') as file:
            file.write(reply)
        with open('mediainfo_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    elif len(reply) != 0:
        message.reply_text(reply, parse_mode='Markdown')
    else:
        message.reply_text('No Reply', parse_mode='Markdown')

def ls(update, context):
    message = update.effective_message
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) == 1:
        cmd = f"ls"
    if len(args) > 1:
        link = args[1]
        cmd = f"ls {shlex.quote(link)}"
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if len(stdout) != 0:
        reply += f"`{stdout}`\n"
        LOGGER.info(f"Ls - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"`{stderr}`\n"
        LOGGER.error(f"Ls - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('ls_output.txt', 'w') as file:
            file.write(reply)
        with open('ls_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    elif len(reply) != 0:
        message.reply_text(reply, parse_mode='Markdown')
    else:
        message.reply_text('No Reply', parse_mode='Markdown')

def rm(update, context):
    message = update.effective_message
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) == 1:
        cmd = f"rm"
    if len(args) > 1:
        link = args[1]
        cmd = f"rm -rf {link}"
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if len(stdout) != 0:
        reply += f"`{stdout}`\n"
        LOGGER.info(f"Rm - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"`{stderr}`\n"
        LOGGER.error(f"Rm - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('rm_output.txt', 'w') as file:
            file.write(reply)
        with open('rm_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    elif len(reply) != 0:
        message.reply_text(reply, parse_mode='Markdown')
    else:
        message.reply_text('Removed', parse_mode='Markdown')

def mv(update, context):
    message = update.effective_message
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) == 1:
        cmd = f"mv"
    if len(args) > 1:
        link = args[1]
        cmd = f"mv {link}"
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if len(stdout) != 0:
        reply += f"`{stdout}`\n"
        LOGGER.info(f"Mv - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"`{stderr}`\n"
        LOGGER.error(f"Mv - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('mv_output.txt', 'w') as file:
            file.write(reply)
        with open('mv_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    elif len(reply) != 0:
        message.reply_text(reply, parse_mode='Markdown')
    else:
        message.reply_text('Moved', parse_mode='Markdown')

def cp(update, context):
    message = update.effective_message
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) == 1:
        cmd = f"cp"
    if len(args) > 1:
        link = args[1]
        cmd = f"cp {link}"
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if len(stdout) != 0:
        reply += f"`{stdout}`\n"
        LOGGER.info(f"Cp - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"`{stderr}`\n"
        LOGGER.error(f"Cp - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('cp_output.txt', 'w') as file:
            file.write(reply)
        with open('cp_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    elif len(reply) != 0:
        message.reply_text(reply, parse_mode='Markdown')
    else:
        message.reply_text('Copied', parse_mode='Markdown')

def mkvextract(update, context):
    message = update.effective_message
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) == 1:
        cmd = f"mkvextract"
    if len(args) > 1:
        link = args[1]
        cmd = f"mkvextract {link}"
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if len(stdout) != 0:
        reply += f"{stdout}\n"
        LOGGER.info(f"Mkvextract - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"{stderr}\n"
        LOGGER.error(f"Mkvextract - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('mkvextract_output.txt', 'w') as file:
            file.write(reply)
        with open('mkvextract_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    elif len(reply) != 0:
        message.reply_text(reply, parse_mode='Markdown')
    else:
        message.reply_text('No Reply', parse_mode='Markdown')

def echo(update, context):
    message = update.effective_message
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) == 1:
        cmd = f"echo"
    if len(args) > 1:
        link = args[1]
        cmd = f"echo {link}"
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if len(stdout) != 0:
        reply += f"`{stdout}`\n"
        LOGGER.info(f"Echo - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"`{stderr}`\n"
        LOGGER.error(f"Echo - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('echo_output.txt', 'w') as file:
            file.write(reply)
        with open('echo_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    elif len(reply) != 0:
        message.reply_text(reply, parse_mode='Markdown')
    else:
        message.reply_text('Done', parse_mode='Markdown')

def curl(update, context):
    message = update.effective_message
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) == 1:
        cmd = f"curl"
    if len(args) > 1:
        link = args[1]
        cmd = f"curl {link}"
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if len(stdout) != 0:
        reply += f"`{stdout}`\n"
        LOGGER.info(f"Curl - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"`{stderr}`\n"
        LOGGER.error(f"Curl - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('curl_output.txt', 'w') as file:
            file.write(reply)
        with open('curl_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    elif len(reply) != 0:
        message.reply_text(reply, parse_mode='Markdown')
    else:
        message.reply_text('No Reply', parse_mode='Markdown')

def mkdir(update, context):
    message = update.effective_message
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) == 1:
        cmd = f"mkdir"
    if len(args) > 1:
        link = args[1]
        cmd = f"mkdir {link}"
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if len(stdout) != 0:
        reply += f"`{stdout}`\n"
        LOGGER.info(f"Mkdir - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"`{stderr}`\n"
        LOGGER.error(f"Mkdir - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('mkdir_output.txt', 'w') as file:
            file.write(reply)
        with open('mkdir_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    elif len(reply) != 0:
        message.reply_text(reply, parse_mode='Markdown')
    else:
        message.reply_text('Done', parse_mode='Markdown')

def ytdlp(update, context):
    message = update.effective_message
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) == 1:
        cmd = f"yt-dlp"
    if len(args) > 1:
        link = args[1]
        cmd = f"yt-dlp {link}"
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if len(stdout) != 0:
        reply += f"`{stdout}`\n"
        LOGGER.info(f"Yt-dlp - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"`{stderr}`\n"
        LOGGER.error(f"Yt-dlp - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('yt-dlp_output.txt', 'w') as file:
            file.write(reply)
        with open('yt-dlp_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    elif len(reply) != 0:
        message.reply_text(reply, parse_mode='Markdown')
    else:
        message.reply_text('No Reply', parse_mode='Markdown')

def python3(update, context):
    message = update.effective_message
    args = update.message.text.split(" ", maxsplit=1)
    link = ''
    if len(args) == 1:
        cmd = f"python3"
    if len(args) > 1:
        link = args[1]
        cmd = f"python3 {link}"
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if len(stdout) != 0:
        reply += f"`{stdout}`\n"
        LOGGER.info(f"Python3 - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"`{stderr}`\n"
        LOGGER.error(f"Python3 - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('python3_output.txt', 'w') as file:
            file.write(reply)
        with open('python3_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    elif len(reply) != 0:
        message.reply_text(reply, parse_mode='Markdown')
    else:
        message.reply_text('Done', parse_mode='Markdown')

ffmpeg_handler = CommandHandler(BotCommands.FfmpegCommand, ffmpeg,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
mkvmerge_handler = CommandHandler(BotCommands.MkvmergeCommand, mkvmerge,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
mediainfo_handler = CommandHandler(BotCommands.MediainfoCommand, mediainfo,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
ls_handler = CommandHandler(BotCommands.LsCommand, ls,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
rm_handler = CommandHandler(BotCommands.RmCommand, rm,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
mv_handler = CommandHandler(BotCommands.MvCommand, mv,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
cp_handler = CommandHandler(BotCommands.CpCommand, cp,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
mkvextract_handler = CommandHandler(BotCommands.MkvextractCommand, mkvextract,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
echo_handler = CommandHandler(BotCommands.EchoCommand, echo,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
curl_handler = CommandHandler(BotCommands.CurlCommand, curl,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
mkdir_handler = CommandHandler(BotCommands.MkdirCommand, mkdir,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
ytdlp_handler = CommandHandler(BotCommands.YtdlpCommand, ytdlp,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
python3_handler = CommandHandler(BotCommands.Python3Command, python3,
                                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
dispatcher.add_handler(ffmpeg_handler)
dispatcher.add_handler(mkvmerge_handler)
dispatcher.add_handler(mediainfo_handler)
dispatcher.add_handler(ls_handler)
dispatcher.add_handler(rm_handler)
dispatcher.add_handler(mv_handler)
dispatcher.add_handler(cp_handler)
dispatcher.add_handler(mkvextract_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(curl_handler)
dispatcher.add_handler(mkdir_handler)
dispatcher.add_handler(ytdlp_handler)
dispatcher.add_handler(python3_handler)
