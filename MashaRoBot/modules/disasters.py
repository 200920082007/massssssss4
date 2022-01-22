import html
import json
import os
from typing import Optional

from MashaRoBot import (
    DEV_USERS,
    OWNER_ID,
    DRAGONS,
    SUPPORT_CHAT,
    DEMONS,
    TIGERS,
    WOLVES,
    dispatcher,
)
from MashaRoBot.modules.helper_funcs.chat_status import (
    dev_plus,
    sudo_plus,
    whitelist_plus,
)
from MashaRoBot.modules.helper_funcs.extraction import extract_user
from MashaRoBot.modules.log_channel import gloggable
from telegram import ParseMode, TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler, run_async
from telegram.utils.helpers import mention_html

ELEVATED_USERS_FILE = os.path.join(os.getcwd(), "MashaRoBot/elevated_users.json")


def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        reply = "That...is a chat! baka ka omae?"

    elif user_id == bot.id:
        reply = "This does not work that way."

    else:
        reply = None
    return reply


# This can serve as a deeplink example.
# disasters =
# """ Text here """

# do not async, not a handler
# def send_disasters(update):
#    update.effective_message.reply_text(
#        disasters, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

### Deep link example ends


@run_async
@dev_plus
@gloggable
def addsudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        message.reply_text("This member is already a Dragon Disaster")
        return ""

    if user_id in DEMONS:
        rt += "Requested HA to promote a Demon Disaster to Dragon."
        data["supports"].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        rt += "Requested HA to promote a Wolf Disaster to Dragon."
        data["whitelists"].remove(user_id)
        WOLVES.remove(user_id)

    data["sudos"].append(user_id)
    DRAGONS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt
        + "\nSuccessfully set Disaster level of {} to Dragon!".format(
            user_member.first_name
        )
    )

    log_message = (
        f"#SUDO\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addsupport(
    update: Update,
    context: CallbackContext,
) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "Requested HA to demote this Dragon to Demon"
        data["sudos"].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        message.reply_text("This user is already a Demon Disaster.")
        return ""

    if user_id in WOLVES:
        rt += "Requested HA to promote this Wolf Disaster to Demon"
        data["whitelists"].remove(user_id)
        WOLVES.remove(user_id)

    data["supports"].append(user_id)
    DEMONS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\n{user_member.first_name} was added as a Demon Disaster!"
    )

    log_message = (
        f"#SUPPORT\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addwhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "This member is a Dragon Disaster, Demoting to Wolf."
        data["sudos"].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        rt += "This user is already a Demon Disaster, Demoting to Wolf."
        data["supports"].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        message.reply_text("This user is already a Wolf Disaster.")
        return ""

    data["whitelists"].append(user_id)
    WOLVES.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\nSuccessfully promoted {user_member.first_name} to a Wolf Disaster!"
    )

    log_message = (
        f"#WHITELIST\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addtiger(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        rt += "This member is a Dragon Disaster, Demoting to Tiger."
        data["sudos"].remove(user_id)
        DRAGONS.remove(user_id)

    if user_id in DEMONS:
        rt += "This user is already a Demon Disaster, Demoting to Tiger."
        data["supports"].remove(user_id)
        DEMONS.remove(user_id)

    if user_id in WOLVES:
        rt += "This user is already a Wolf Disaster, Demoting to Tiger."
        data["whitelists"].remove(user_id)
        WOLVES.remove(user_id)

    if user_id in TIGERS:
        message.reply_text("This user is already a Tiger.")
        return ""

    data["tigers"].append(user_id)
    TIGERS.append(user_id)

    with open(ELEVATED_USERS_FILE, "w") as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\nSuccessfully promoted {user_member.first_name} to a Tiger Disaster!"
    )

    log_message = (
        f"#TIGER\n"
        f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))} \n"
        f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
    )

    if chat.type != "private":
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@dev_plus
@gloggable
def removesudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DRAGONS:
        message.reply_text("Requested HA to demote this user to Civilian")
        DRAGONS.remove(user_id)
        data["sudos"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNSUDO\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = "<b>{}:</b>\n".format(html.escape(chat.title)) + log_message

        return log_message

    else:
        message.reply_text("This user is not a Dragon Disaster!")
        return ""


@run_async
@sudo_plus
@gloggable
def removesupport(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in DEMONS:
        message.reply_text("Requested HA to demote this user to Civilian")
        DEMONS.remove(user_id)
        data["supports"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNSUPPORT\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message

    else:
        message.reply_text("This user is not a Demon level Disaster!")
        return ""


@run_async
@sudo_plus
@gloggable
def removewhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in WOLVES:
        message.reply_text("Demoting to normal user")
        WOLVES.remove(user_id)
        data["whitelists"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNWHITELIST\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a Wolf Disaster!")
        return ""


@run_async
@sudo_plus
@gloggable
def removetiger(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, "r") as infile:
        data = json.load(infile)

    if user_id in TIGERS:
        message.reply_text("Demoting to normal user")
        TIGERS.remove(user_id)
        data["tigers"].remove(user_id)

        with open(ELEVATED_USERS_FILE, "w") as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNTIGER\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            f"<b>User:</b> {mention_html(user_member.id, html.escape(user_member.first_name))}"
        )

        if chat.type != "private":
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a Tiger Disaster!")
        return ""


@run_async
@whitelist_plus
def whitelistlist(update: Update, context: CallbackContext):
    reply = "<b>Known Wolf Disasters 🐺:</b>\n"
    m = update.effective_message.reply_text(
        "<code>Gathering intel..</code>", parse_mode=ParseMode.HTML
    )
    bot = context.bot
    for each_user in WOLVES:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)

            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def tigerlist(update: Update, context: CallbackContext):
    reply = "<b>Known Tiger Disasters 🐯:</b>\n"
    m = update.effective_message.reply_text(
        "<code>Gathering intel..</code>", parse_mode=ParseMode.HTML
    )
    bot = context.bot
    for each_user in TIGERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def supportlist(update: Update, context: CallbackContext):
    bot = context.bot
    m = update.effective_message.reply_text(
        "<code>Gathering intel..</code>", parse_mode=ParseMode.HTML
    )
    reply = "<b>Known Demon Disasters 👹:</b>\n"
    for each_user in DEMONS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def sudolist(update: Update, context: CallbackContext):
    bot = context.bot
    m = update.effective_message.reply_text(
        "<code>Gathering intel..</code>", parse_mode=ParseMode.HTML
    )
    true_sudo = list(set(DRAGONS) - set(DEV_USERS))
    reply = "<b>Known Dragon Disasters 🐉:</b>\n"
    for each_user in true_sudo:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def devlist(update: Update, context: CallbackContext):
    bot = context.bot
    m = update.effective_message.reply_text(
        "<code>Gathering intel..</code>", parse_mode=ParseMode.HTML
    )
    true_dev = list(set(DEV_USERS) - {OWNER_ID})
    reply = "<b>Hero Association Members ⚡️:</b>\n"
    for each_user in true_dev:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, html.escape(user.first_name))}\n"
        except TelegramError:
            pass
    m.edit_text(reply, parse_mode=ParseMode.HTML)


__help__ = f"""
*⚠️ Notice:*
Cᴏᴍᴍᴀɴᴅs ʟɪsᴛᴇᴅ ʜᴇʀᴇ ᴏɴʟʏ ᴡᴏʀᴋ ғᴏʀ ᴜsᴇʀs ᴡɪᴛʜ sᴘᴇᴄɪᴀʟ ᴀᴄᴄᴇss ᴀʀᴇ ᴍᴀɪɴʟʏ ᴜsᴇᴅ ғᴏʀ ᴛʀᴏᴜʙʟᴇsʜᴏᴏᴛɪɴɢ, ᴅᴇʙᴜɢɢɪɴɢ ᴘᴜʀᴘᴏsᴇs.
Gʀᴏᴜᴘ ᴀᴅᴍɪɴs/ɢʀᴏᴜᴘ ᴏᴡɴᴇʀs ᴅᴏ ɴᴏᴛ ɴᴇᴇᴅ ᴛʜᴇsᴇ ᴄᴏᴍᴍᴀɴᴅs. 

*Lɪsᴛ ᴀʟʟ sᴘᴇᴄɪᴀʟ ᴜsᴇʀs:*
 ❍ /dragons*:* Lɪsᴛs ᴀʟʟ Dʀᴀɢᴏɴ ᴅɪsᴀsᴛᴇʀs
 ❍ /demons*:* Lɪsᴛs ᴀʟʟ Dᴇᴍᴏɴ ᴅɪsᴀsᴛᴇʀs
 ❍ /tigers*:* Lɪsᴛs ᴀʟʟ Tɪɢᴇʀs ᴅɪsᴀsᴛᴇʀs
 ❍ /wolves*:* Lɪsᴛs ᴀʟʟ Wᴏʟғ ᴅɪsᴀsᴛᴇʀs
 ❍ /heroes*:* Lɪsᴛs ᴀʟʟ Hᴇʀᴏ Assᴏᴄɪᴀᴛɪᴏɴ ᴍᴇᴍʙᴇʀs
 ❍ /adddragon*:* Aᴅᴅs ᴀ ᴜsᴇʀ ᴛᴏ Dʀᴀɢᴏɴ
 ❍ /adddemon*:* Aᴅᴅs ᴀ ᴜsᴇʀ ᴛᴏ Dᴇᴍᴏɴ
 ❍ /addtiger*:* Aᴅᴅs ᴀ ᴜsᴇʀ ᴛᴏ Tɪɢᴇʀ
 ❍ /addwolf*:* Aᴅᴅs ᴀ ᴜsᴇʀ ᴛᴏ Wᴏʟғ
 ❍ `Aᴅᴅ ᴅᴇᴠ ᴅᴏᴇsɴᴛ ᴇxɪsᴛ, ᴅᴇᴠs sʜᴏᴜʟᴅ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ ᴀᴅᴅ ᴛʜᴇᴍsᴇʟᴠᴇs`

*Pɪɴɢ:*
 ❍ /ping*:* ɢᴇᴛs ᴘɪɴɢ ᴛɪᴍᴇ ᴏғ ʙᴏᴛ ᴛᴏ ᴛᴇʟᴇɢʀᴀᴍ sᴇʀᴠᴇʀ
 ❍ /pingall*:* ɢᴇᴛs ᴀʟʟ ʟɪsᴛᴇᴅ ᴘɪɴɢ ᴛɪᴍᴇs

*Bʀᴏᴀᴅᴄᴀsᴛ: (Bᴏᴛ ᴏᴡɴᴇʀ ᴏɴʟʏ)*
*Nᴏᴛᴇ:* Tʜɪs sᴜᴘᴘᴏʀᴛs ʙᴀsɪᴄ ᴍᴀʀᴋᴅᴏᴡɴ
 ❍ /broadcastall*:* Bʀᴏᴀᴅᴄᴀsᴛs ᴇᴠᴇʀʏᴡʜᴇʀᴇ
 ❍ /broadcastusers*:* Bʀᴏᴀᴅᴄᴀsᴛs ᴛᴏᴏ ᴀʟʟ ᴜsᴇʀs
 ❍ /broadcastgroups*:* Bʀᴏᴀᴅᴄᴀsᴛs ᴛᴏᴏ ᴀʟʟ ɢʀᴏᴜᴘs

*Gʀᴏᴜᴘs Iɴғᴏ:*
 ❍ /groups*:* Lɪsᴛ ᴛʜᴇ ɢʀᴏᴜᴘs ᴡɪᴛʜ Nᴀᴍᴇ, ID, ᴍᴇᴍʙᴇʀs ᴄᴏᴜɴᴛ ᴀs ᴀ ᴛxᴛ
 ❍ /leave <ID>*:* Lᴇᴀᴠᴇ ᴛʜᴇ ɢʀᴏᴜᴘ, ID ᴍᴜsᴛ ʜᴀᴠᴇ ʜʏᴘʜᴇɴ
 ❍ /stats*:* Sʜᴏᴡs ᴏᴠᴇʀᴀʟʟ ʙᴏᴛ sᴛᴀᴛs
 ❍ /getchats*:* Gᴇᴛs ᴀ ʟɪsᴛ ᴏғ ɢʀᴏᴜᴘ ɴᴀᴍᴇs ᴛʜᴇ ᴜsᴇʀ ʜᴀs ʙᴇᴇɴ sᴇᴇɴ ɪɴ. Bᴏᴛ ᴏᴡɴᴇʀ ᴏɴʟʏ
 ❍ /ginfo ᴜsᴇʀɴᴀᴍᴇ/ʟɪɴᴋ/ID*:* Pᴜʟʟs ɪɴғᴏ ᴘᴀɴᴇʟ ғᴏʀ ᴇɴᴛɪʀᴇ ɢʀᴏᴜᴘ

*Aᴄᴄᴇss ᴄᴏɴᴛʀᴏʟ:* 
 ❍ /ignore*:* Bʟᴀᴄᴋʟɪsᴛs ᴀ ᴜsᴇʀ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ ᴇɴᴛɪʀᴇʟʏ
 ❍ /lockdown <ᴏғғ/ᴏɴ>*:* Tᴏɢɢʟᴇs ʙᴏᴛ ᴀᴅᴅɪɴɢ ᴛᴏ ɢʀᴏᴜᴘs
 ❍ /notice*:* Rᴇᴍᴏᴠᴇs ᴜsᴇʀ ғʀᴏᴍ ʙʟᴀᴄᴋʟɪsᴛ
 ❍ /ignoredlist*:* Lɪsᴛs ɪɢɴᴏʀᴇᴅ ᴜsᴇʀs

*Sᴘᴇᴇᴅᴛᴇsᴛ:*
 ❍ /speedtest*:* Rᴜɴs ᴀ sᴘᴇᴇᴅᴛᴇsᴛ ᴀɴᴅ ɢɪᴠᴇs ʏᴏᴜ 2 ᴏᴘᴛɪᴏɴs ᴛᴏ ᴄʜᴏᴏsᴇ ғʀᴏᴍ, ᴛᴇxᴛ ᴏʀ ɪᴍᴀɢᴇ ᴏᴜᴛᴘᴜᴛ

*Mᴏᴅᴜʟᴇ ʟᴏᴀᴅɪɴɢ:*
 ❍ /listmodules*:* Lɪsᴛs ɴᴀᴍᴇs ᴏғ ᴀʟʟ ᴍᴏᴅᴜʟᴇs
 ❍ /loadmodulename*:* Lᴏᴀᴅs ᴛʜᴇ sᴀɪᴅ ᴍᴏᴅᴜʟᴇ ᴛᴏ ᴍᴇᴍᴏʀʏ ᴡɪᴛʜᴏᴜᴛ ʀᴇsᴛᴀʀᴛɪɴɢ.
 ❍ /unloadmodulename*:* Lᴏᴀᴅs ᴛʜᴇ sᴀɪᴅ ᴍᴏᴅᴜʟᴇ ғʀᴏᴍᴍᴇᴍᴏʀʏ ᴡɪᴛʜᴏᴜᴛ ʀᴇsᴛᴀʀᴛɪɴɢ ᴍᴇᴍᴏʀʏ ᴡɪᴛʜᴏᴜᴛ ʀᴇsᴛᴀʀᴛɪɴɢ ᴛʜᴇ ʙᴏᴛ 

*Rᴇᴍᴏᴛᴇ ᴄᴏᴍᴍᴀɴᴅs:*
 ❍ /rban*:* ᴜsᴇʀ ɢʀᴏᴜᴘ*:* Rᴇᴍᴏᴛᴇ ʙᴀɴ
 ❍ /runban*:* ᴜsᴇʀ ɢʀᴏᴜᴘ*:* Rᴇᴍᴏᴛᴇ ᴜɴ-ʙᴀɴ
 ❍ /rpunch*:* ᴜsᴇʀ ɢʀᴏᴜᴘ*:* Rᴇᴍᴏᴛᴇ ᴘᴜɴᴄʜ
 ❍ /rmute*:* ᴜsᴇʀ ɢʀᴏᴜᴘ*:* Rᴇᴍᴏᴛᴇ ᴍᴜᴛᴇ
 ❍ /runmute*:* ᴜsᴇʀ ɢʀᴏᴜᴘ*:* Rᴇᴍᴏᴛᴇ ᴜɴ-ᴍᴜᴛᴇ

*Wɪɴᴅᴏᴡs sᴇʟғ ʜᴏsᴛᴇᴅ ᴏɴʟʏ:*
 ❍ /reboot*:* Rᴇsᴛᴀʀᴛs ᴛʜᴇ ʙᴏᴛs sᴇʀᴠɪᴄᴇ
 ❍ /gitpull*:* Pᴜʟʟs ᴛʜᴇ ʀᴇᴘᴏ ᴀɴᴅ ᴛʜᴇɴ ʀᴇsᴛᴀʀᴛs ᴛʜᴇ ʙᴏᴛs sᴇʀᴠɪᴄᴇ

*Cʜᴀᴛʙᴏᴛ:* 
 ❍ /listaichats*:* Lɪsᴛs ᴛʜᴇ ᴄʜᴀᴛs ᴛʜᴇ ᴄʜᴀᴛᴍᴏᴅᴇ ɪs ᴇɴᴀʙʟᴇᴅ ɪɴ
 
*Dᴇʙᴜɢɢɪɴɢ ᴀɴᴅ Sʜᴇʟʟ:* 
 ❍ /debug <ᴏɴ/ᴏғғ>*:* Lᴏɢs ᴄᴏᴍᴍᴀɴᴅs ᴛᴏ ᴜᴘᴅᴀᴛᴇs.ᴛxᴛ
 ❍ /logs*:* Rᴜɴ ᴛʜɪs ɪɴ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ ᴛᴏ ɢᴇᴛ ʟᴏɢs ɪɴ ᴘᴍ
 ❍ /eval*:* Sᴇʟғ ᴇxᴘʟᴀɴᴀᴛᴏʀʏ
 ❍ /sh*:* Rᴜɴs sʜᴇʟʟ ᴄᴏᴍᴍᴀɴᴅ
 ❍ /shell*:* Rᴜɴs sʜᴇʟʟ ᴄᴏᴍᴍᴀɴᴅ
 ❍ /clearlocals*:* As ᴛʜᴇ ɴᴀᴍᴇ ɢᴏᴇs
 ❍ /dbcleanup*:* Rᴇᴍᴏᴠᴇs ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄs ᴀɴᴅ ɢʀᴏᴜᴘs ғʀᴏᴍ ᴅʙ
 ❍ /py*:* Rᴜɴs ᴘʏᴛʜᴏɴ ᴄᴏᴅᴇ
 
*Gʟᴏʙᴀʟ Bᴀɴs:*
 ❍ /gban<ɪᴅ> <ʀᴇᴀsᴏɴ>*:* Gʙᴀɴs ᴛʜᴇ ᴜsᴇʀ, ᴡᴏʀᴋs ʙʏ ʀᴇᴘʟʏ ᴛᴏᴏ
 ❍ /ungban*:* Uɴɢʙᴀɴs ᴛʜᴇ ᴜsᴇʀ, sᴀᴍᴇ ᴜsᴀɢᴇ ᴀs ɢʙᴀɴ
 ❍ /gbanlist*:* Oᴜᴛᴘᴜᴛs ᴀ ʟɪsᴛ ᴏғ ɢʙᴀɴɴᴇᴅ ᴜsᴇʀs

*Gʟᴏʙᴀʟ Bʟᴜᴇ Tᴇxᴛ*
 ❍ /gignoreblue*:* <ᴡᴏʀᴅ>*:* Gʟᴏʙᴀʟʟʏ ɪɢɴᴏʀᴇᴀ ʙʟᴜᴇᴛᴇxᴛ ᴄʟᴇᴀɴɪɴɢ ᴏғ sᴀᴠᴇᴅ ᴡᴏʀᴅ ᴀᴄʀᴏss MᴀsʜᴀRᴏBᴏᴛ.
 ❍ /ungignoreblue*:* <ᴡᴏʀᴅ>*:* Rᴇᴍᴏᴠᴇ sᴀɪᴅ ᴄᴏᴍᴍᴀɴᴅ ғʀᴏᴍ ɢʟᴏʙᴀʟ ᴄʟᴇᴀɴɪɴɢ ʟɪsᴛ

*Mᴀsʜᴀ Cᴏʀᴇ*
*Oᴡɴᴇʀ ᴏɴʟʏ*
 ❍ /send*:* <ᴍᴏᴅᴜʟᴇ ɴᴀᴍᴇ>*:* Sᴇɴᴅ ᴍᴏᴅᴜʟᴇ
 ❍ /install*:* <ʀᴇᴘʟʏ ᴛᴏ ᴀ .ᴘʏ>*:* Iɴsᴛᴀʟʟ ᴍᴏᴅᴜʟᴇ 

*Hᴇʀᴏᴋᴜ Sᴇᴛᴛɪɴɢs*
*Oᴡɴᴇʀ ᴏɴʟʏ*
 ❍ /usage*:* Cʜᴇᴄᴋ ʏᴏᴜʀ ʜᴇʀᴏᴋᴜ ᴅʏɴᴏ ʜᴏᴜʀs ʀᴇᴍᴀɪɴɪɴɢ.
 ❍ /seevar <ᴠᴀʀ>*:* Gᴇᴛ ʏᴏᴜʀ ᴇxɪsᴛɪɴɢ ᴠᴀʀɪʙʟᴇs, ᴜsᴇ ɪᴛ ᴏɴʟʏ ᴏɴ ʏᴏᴜʀ ᴘʀɪᴠᴀᴛᴇ ɢʀᴏᴜᴘ!
 ❍ /setwar <ɴᴇᴡᴠᴀʀ> <ᴠᴀᴠᴀʀɪᴀʙʟᴇ>*:* Aᴅᴅ ɴᴇᴡ ᴠᴀʀɪᴀʙʟᴇ ᴏʀ ᴜᴘᴅᴀᴛᴇ ᴇxɪsᴛɪɴɢ ᴠᴀʟᴜᴇ ᴠᴀʀɪᴀʙʟᴇ.
 ❍ /delwar <ᴠᴀʀ>*:* Dᴇʟᴇᴛᴇ ᴇxɪsᴛɪɴɢ ᴠᴀʀɪᴀʙʟᴇ.
 ❍ /logs Gᴇᴛ ʜᴇʀᴏᴋᴜ ᴅʏɴᴏ ʟᴏɢs.

`⚠️ Rᴇᴀᴅ ғʀᴏᴍ ᴛᴏᴘ`
Vɪsɪᴛ *@Mksupport1* ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.
"""

SUDO_HANDLER = CommandHandler(("addsudo", "adddragon"), addsudo)
SUPPORT_HANDLER = CommandHandler(("addsupport", "adddemon"), addsupport)
TIGER_HANDLER = CommandHandler(("addtiger"), addtiger)
WHITELIST_HANDLER = CommandHandler(("addwhitelist", "addwolf"), addwhitelist)
UNSUDO_HANDLER = CommandHandler(("removesudo", "removedragon"), removesudo)
UNSUPPORT_HANDLER = CommandHandler(("removesupport", "removedemon"), removesupport)
UNTIGER_HANDLER = CommandHandler(("removetiger"), removetiger)
UNWHITELIST_HANDLER = CommandHandler(("removewhitelist", "removewolf"), removewhitelist)

WHITELISTLIST_HANDLER = CommandHandler(["whitelistlist", "wolves"], whitelistlist)
TIGERLIST_HANDLER = CommandHandler(["tigers"], tigerlist)
SUPPORTLIST_HANDLER = CommandHandler(["supportlist", "demons"], supportlist)
SUDOLIST_HANDLER = CommandHandler(["sudolist", "dragons"], sudolist)
DEVLIST_HANDLER = CommandHandler(["devlist", "heroes"], devlist)

dispatcher.add_handler(SUDO_HANDLER)
dispatcher.add_handler(SUPPORT_HANDLER)
dispatcher.add_handler(TIGER_HANDLER)
dispatcher.add_handler(WHITELIST_HANDLER)
dispatcher.add_handler(UNSUDO_HANDLER)
dispatcher.add_handler(UNSUPPORT_HANDLER)
dispatcher.add_handler(UNTIGER_HANDLER)
dispatcher.add_handler(UNWHITELIST_HANDLER)

dispatcher.add_handler(WHITELISTLIST_HANDLER)
dispatcher.add_handler(TIGERLIST_HANDLER)
dispatcher.add_handler(SUPPORTLIST_HANDLER)
dispatcher.add_handler(SUDOLIST_HANDLER)
dispatcher.add_handler(DEVLIST_HANDLER)

__mod_name__ = "Ꮇ-ᎬХͲᎡᎪ🛷"
__handlers__ = [
    SUDO_HANDLER,
    SUPPORT_HANDLER,
    TIGER_HANDLER,
    WHITELIST_HANDLER,
    UNSUDO_HANDLER,
    UNSUPPORT_HANDLER,
    UNTIGER_HANDLER,
    UNWHITELIST_HANDLER,
    WHITELISTLIST_HANDLER,
    TIGERLIST_HANDLER,
    SUPPORTLIST_HANDLER,
    SUDOLIST_HANDLER,
    DEVLIST_HANDLER,
]
