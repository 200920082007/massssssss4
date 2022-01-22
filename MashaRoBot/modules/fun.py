import html

import random

import time

from typing import Optional

from telegram import ParseMode, Update, ChatPermissions

from telegram.ext import CallbackContext, run_async

from tswift import Song

from telegram.error import BadRequest

import MashaRoBot.modules.fun_strings as fun_strings

from MashaRoBot import dispatcher

from MashaRoBot.modules.disable import DisableAbleCommandHandler

from MashaRoBot.modules.helper_funcs.alternate import send_message, typing_action

from MashaRoBot.modules.helper_funcs.chat_status import (is_user_admin)

from MashaRoBot.modules.helper_funcs.extraction import extract_user

GIF_ID = 'CgACAgQAAx0CSVUvGgAC7KpfWxMrgGyQs-GUUJgt-TSO8cOIDgACaAgAAlZD0VHT3Zynpr5nGxsE'

@run_async

def runs(update: Update, context: CallbackContext):

    update.effective_message.reply_text(random.choice(fun_strings.RUN_STRINGS))

@run_async

def sanitize(update: Update, context: CallbackContext):

    message = update.effective_message

    name = message.reply_to_message.from_user.first_name if message.reply_to_message else message.from_user.first_name

    reply_animation = message.reply_to_message.reply_animation if message.reply_to_message else message.reply_animation

    reply_animation(GIF_ID, caption=f'*Sanitizes {name}*')

@run_async

def sanitize(update: Update, context: CallbackContext):

    message = update.effective_message

    name = message.reply_to_message.from_user.first_name if message.reply_to_message else message.from_user.first_name

    reply_animation = message.reply_to_message.reply_animation if message.reply_to_message else message.reply_animation

    reply_animation(

        random.choice(fun_strings.GIFS), caption=f'*Sanitizes {name}*')

@run_async

def eightball(update: Update, context: CallbackContext):

    reply_text = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text

    reply_text(random.choice(fun_strings.EIGHTBALL))

@run_async

def slap(update: Update, context: CallbackContext):

    bot, args = context.bot, context.args

    message = update.effective_message

    chat = update.effective_chat

    reply_text = message.reply_to_message.reply_text if message.reply_to_message else message.reply_text

    curr_user = html.escape(message.from_user.first_name)

    user_id = extract_user(message, args)

    if user_id == bot.id:

        temp = random.choice(fun_strings.SLAP_MASHA_TEMPLATES)

        if isinstance(temp, list):

            if temp[2] == "tmute":

                if is_user_admin(chat, message.from_user.id):

                    reply_text(temp[1])

                    return

                mutetime = int(time.time() + 60)

                bot.restrict_chat_member(

                    chat.id,

                    message.from_user.id,

                    until_date=mutetime,

                    permissions=ChatPermissions(can_send_messages=False))

            reply_text(temp[0])

        else:

            reply_text(temp)

        return

    if user_id:

        slapped_user = bot.get_chat(user_id)

        user1 = curr_user

        user2 = html.escape(slapped_user.first_name)

    else:

        user1 = bot.first_name

        user2 = curr_user

    temp = random.choice(fun_strings.SLAP_TEMPLATES)

    item = random.choice(fun_strings.ITEMS)

    hit = random.choice(fun_strings.HIT)

    throw = random.choice(fun_strings.THROW)

    if update.effective_user.id == 1410092658:

        temp = ".... scratches {user2}"

        

    reply = temp.format(

        user1=user1, user2=user2, item=item, hits=hit, throws=throw)

    reply_text(reply, parse_mode=ParseMode.HTML)

@run_async

def pat(update: Update, context: CallbackContext):

    bot = context.bot

    args = context.args

    message = update.effective_message

    reply_to = message.reply_to_message if message.reply_to_message else message

    curr_user = html.escape(message.from_user.first_name)

    user_id = extract_user(message, args)

    if user_id:

        patted_user = bot.get_chat(user_id)

        user1 = curr_user

        user2 = html.escape(patted_user.first_name)

    else:

        user1 = bot.first_name

        user2 = curr_user

    pat_type = random.choice(("Text", "Gif", "Sticker"))

    if pat_type == "Gif":

        try:

            temp = random.choice(fun_strings.PAT_GIFS)

            reply_to.reply_animation(temp)

        except BadRequest:

            pat_type = "Text"

    if pat_type == "Sticker":

        try:

            temp = random.choice(fun_strings.PAT_STICKERS)

            reply_to.reply_sticker(temp)

        except BadRequest:

            pat_type = "Text"

    if pat_type == "Text":

        temp = random.choice(fun_strings.PAT_TEMPLATES)

        reply = temp.format(user1=user1, user2=user2)

        reply_to.reply_text(reply, parse_mode=ParseMode.HTML)

@run_async

@typing_action

def lyrics(update: Update, context: CallbackContext):

    bot, args = context.bot, context.args

    msg = update.effective_message

    query = " ".join(args)

    song = ""

    if not query:

        msg.reply_text("You haven't specified which song to look for!")

        return

    song = Song.find_song(query)

    if song:

        if song.lyrics:

            reply = song.format()

        else:

            reply = "Couldn't find any lyrics for that song!"

    else:

        reply = "Song not found!"

    if len(reply) > 4090:

        with open("lyrics.txt", 'w') as f:

            f.write(f"{reply}\n\n\nOwO UwU OmO")

        with open("lyrics.txt", 'rb') as f:

            msg.reply_document(document=f,

            caption="Message length exceeded max limit! Sending as a text file.")

    else:

        msg.reply_text(reply)

@run_async

def roll(update: Update, context: CallbackContext):

    update.message.reply_text(random.choice(range(1, 7)))

@run_async

def toss(update: Update, context: CallbackContext):

    update.message.reply_text(random.choice(fun_strings.TOSS))

@run_async

def shrug(update: Update, context: CallbackContext):

    msg = update.effective_message

    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    reply_text(r"¯\_(ツ)_/¯")

@run_async

def bluetext(update: Update, context: CallbackContext):

    msg = update.effective_message

    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    reply_text(

        "/BLUE /TEXT\n/MUST /CLICK\n/I /AM /A /STUPID /ANIMAL /THAT /IS /ATTRACTED /TO /COLORS"

    )

@run_async

def rlg(update: Update, context: CallbackContext):

    eyes = random.choice(fun_strings.EYES)

    mouth = random.choice(fun_strings.MOUTHS)

    ears = random.choice(fun_strings.EARS)

    if len(eyes) == 2:

        repl = ears[0] + eyes[0] + mouth[0] + eyes[1] + ears[1]

    else:

        repl = ears[0] + eyes[0] + mouth[0] + eyes[0] + ears[1]

    update.message.reply_text(repl)

@run_async

def decide(update: Update, context: CallbackContext):

    reply_text = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text

    reply_text(random.choice(fun_strings.DECIDE))

@run_async

def table(update: Update, context: CallbackContext):

    reply_text = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text

    reply_text(random.choice(fun_strings.TABLE))

normiefont = [

    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',

    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'

]

weebyfont = [

    '卂', '乃', '匚', '刀', '乇', '下', '厶', '卄', '工', '丁', '长', '乚', '从', '𠘨', '口',

    '尸', '㔿', '尺', '丂', '丅', '凵', 'リ', '山', '乂', '丫', '乙'

]

@run_async

def weebify(update: Update, context: CallbackContext):

    args = context.args

    message = update.effective_message

    string = ""

    if message.reply_to_message:

        string = message.reply_to_message.text.lower().replace(" ", "  ")

    if args:

        string = '  '.join(args).lower()

    if not string:

        message.reply_text(

            "Usage is `/weebify <text>`", parse_mode=ParseMode.MARKDOWN)

        return

    for normiecharacter in string:

        if normiecharacter in normiefont:

            weebycharacter = weebyfont[normiefont.index(normiecharacter)]

            string = string.replace(normiecharacter, weebycharacter)

    if message.reply_to_message:

        message.reply_to_message.reply_text(string)

    else:

        message.reply_text(string)

__help__ = """

 • `/runs `*:* ʀᴇᴘʟʏ ᴀ ʀᴀɴᴅᴏᴍ sᴛʀɪɴɢ ғʀᴏᴍ ᴀɴ ᴀʀʀᴀʏ ᴏғ ʀᴇᴘʟɪᴇs

 • `/slap `*:* sʟᴀᴘ ᴀ ᴜsᴇʀ, ᴏʀ ɢᴇᴛ sʟᴀᴘᴘᴇᴅ ɪғ ɴᴏᴛ ᴀ ʀᴇᴘʟʏ

 • `/shrug `*:* ɢᴇᴛ sʜʀᴜɢ XD

 • `/table `*:* ɢᴇᴛ ғʟɪᴘ/ᴜɴғʟɪᴘ :ᴠ

 • `/decide `*:* Rᴀɴᴅᴏᴍʟʏ ᴀɴsᴡᴇʀs ʏᴇs/ɴᴏ/ᴍᴀʏʙᴇ

 • `/toss `*:* Tᴏssᴇs A ᴄᴏɪɴ

 • `/bluetext *:* ᴄʜᴇᴄᴋ ᴜʀsᴇʟғ :V

 • `/roll `*:* Rᴏʟʟ ᴀ ᴅɪᴄᴇ

 • `/rlg `*:* Jᴏɪɴ ᴇᴀʀs,ɴᴏsᴇ,ᴍᴏᴜᴛʜ ᴀɴᴅ ᴄʀᴇᴀᴛᴇ ᴀɴ ᴇᴍᴏ ;-;

 • `/shout <ᴋᴇʏᴡᴏʀᴅ>`*:* ᴡʀɪᴛᴇ ᴀɴʏᴛʜɪɴɢ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɢɪᴠᴇ ʟᴏᴜᴅ sʜᴏᴜᴛ

 • `/weebify <ᴛᴇxᴛ>`*:* ʀᴇᴛᴜʀɴs ᴀ ᴡᴇᴇʙɪғɪᴇᴅ ᴛᴇxᴛ

 • `/truth `*:* ғᴏʀ ʀᴀɴᴅᴏᴍ ᴛʀᴜᴛʜ

 • `/dare `*:* ғᴏʀ ʀᴀɴᴅᴏᴍ ᴅᴀʀᴇ

 • `/sanitize`*:* ᴀʟᴡᴀʏs ᴜsᴇ ᴛʜɪs ʙᴇғᴏʀᴇ /ᴘᴀᴛ ᴏʀ ᴀɴʏ ᴄᴏɴᴛᴀᴄᴛ

 • `/pat `*:* ᴘᴀᴛs ᴀ ᴜsᴇʀ, ᴏʀ ɢᴇᴛ ᴘᴀᴛᴛᴇᴅ

 • `/fun `*:* ғᴜɴɴʏ ᴛᴇxᴛ,sᴛʀɪᴄᴋᴇʀ ᴀɴᴅ ɢɪғ sᴇɴᴅ

 • `/aq`*:* ɢᴇᴛ ʀᴀɴᴅᴏᴍ ᴀɴɪᴍᴇ ϙᴜᴏᴛᴇ

 • `/lyrics <sᴏɴɢ ɴᴀᴍᴇ> `*:* ᴛᴇxᴛ ᴛᴏ ᴠᴏɪᴄᴇ

 • `/plet <ᴛᴇxᴛ> `*:* ᴛᴇxᴛ ɢᴇᴛ ғᴜɴɴʏ ᴇᴍᴏᴊɪғʏ

 • `/tts <ᴛᴇxᴛ> `*:* ᴛᴇxᴛ ᴛᴏ ᴠᴏɪᴄᴇ

 • `/8ball `*:* ᴘʀᴇᴅɪᴄᴛs ᴜsɪɴɢ 8ʙᴀʟʟ ᴍᴇᴛʜᴏᴅ

"""

SANITIZE_HANDLER = DisableAbleCommandHandler("sanitize", sanitize)

RUNS_HANDLER = DisableAbleCommandHandler("runs", runs)

SLAP_HANDLER = DisableAbleCommandHandler("slap", slap)

PAT_HANDLER = DisableAbleCommandHandler("pat", pat)

ROLL_HANDLER = DisableAbleCommandHandler("roll", roll)

TOSS_HANDLER = DisableAbleCommandHandler("toss", toss)

SHRUG_HANDLER = DisableAbleCommandHandler("shrug", shrug)

BLUETEXT_HANDLER = DisableAbleCommandHandler("bluetext", bluetext)

RLG_HANDLER = DisableAbleCommandHandler("rlg", rlg)

DECIDE_HANDLER = DisableAbleCommandHandler("decide", decide)

EIGHTBALL_HANDLER = DisableAbleCommandHandler("8ball", eightball)

LYRICS_HANDLER = DisableAbleCommandHandler("lyrics", lyrics)

TABLE_HANDLER = DisableAbleCommandHandler("table", table)

WEEBIFY_HANDLER = DisableAbleCommandHandler("weebify", weebify)

dispatcher.add_handler(SANITIZE_HANDLER)

dispatcher.add_handler(RUNS_HANDLER)

dispatcher.add_handler(SLAP_HANDLER)

dispatcher.add_handler(PAT_HANDLER)

dispatcher.add_handler(ROLL_HANDLER)

dispatcher.add_handler(TOSS_HANDLER)

dispatcher.add_handler(LYRICS_HANDLER)

dispatcher.add_handler(SHRUG_HANDLER)

dispatcher.add_handler(EIGHTBALL_HANDLER)

dispatcher.add_handler(BLUETEXT_HANDLER)

dispatcher.add_handler(RLG_HANDLER)

dispatcher.add_handler(DECIDE_HANDLER)

dispatcher.add_handler(TABLE_HANDLER)

dispatcher.add_handler(WEEBIFY_HANDLER)

__mod_name__ = "ҒႮΝ😂"

__command_list__ = [

    "runs", "slap", "roll", "toss", "shrug", "bluetext", "rlg", "decide",

    "table", "pat", "sanitize", "lyrics", "weebify",

]

__handlers__ = [

    RUNS_HANDLER, SLAP_HANDLER, PAT_HANDLER, ROLL_HANDLER, TOSS_HANDLER,

    SHRUG_HANDLER, BLUETEXT_HANDLER, RLG_HANDLER, DECIDE_HANDLER, TABLE_HANDLER,

    SANITIZE_HANDLER, LYRICS_HANDLER, EIGHTBALL_HANDLER, WEEBIFY_HANDLER

]
