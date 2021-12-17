# U S Σ R Δ T O R / Coshgyn

from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights, MessageEntityMentionName
from userbot import bot 
from userbot.events import register
from userbot.cmdhelp import CmdHelp

async def get_full_user(event):
    user = event.pattern_match.group(1).split(":", 1)
    extra = None
    if event.reply_to_msg_id and not len(user) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif len(user[0]) > 0:
        user = user[0]
        if len(user) == 2:
            extra = user[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`Bu əmr ID olmadan həyata keçirilə bilməz`")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await event.edit(
                "Bir xəta baş verdi:\nBunu @UseratorSUP’a bildirin", str(err)
            )
    return user_obj, extra

global amdin, sahib
amdin = "admin"
sahib = "owner"


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj


@register(outgoing=True, pattern="^.gpromote ?(.*)")
async def gpromote(event):
    event= event = event
    i = 0
    await event.get_sender()
    me = await event.client.get_me()
    await event.edit("`İcazə verilir...`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await event.get_chat()
    if event.is_private:
        user = event.chat
        rank = event.pattern_match.group(1)
    else:
        event.chat.title
    try:
        user, rank = await get_full_user(event)
    except:
        pass
    if me == user:
        await event.edit("Hey! Özün özünü admin edə bilməzsən :d")
        return
    try:
        if not rank:
            rank = "ㅤㅤ"
    except:
        return await event.edit(f"**Bir xəta baş verdi**")
    if user:
        telchanel = [
            d.entity.id
            for d in await event.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        rgt = ChatAdminRights(
            add_admins=False,
            invite_users=True,
            change_info=False,
            ban_users=True,
            delete_messages=True,
            pin_messages=True,
        )
        for x in telchanel:
            try:
                await event.client(EditAdminRequest(x, user, rgt, rank))
                i += 1
                await event.edit(f"**Admin əlavə etmə səlahiyyətin olduğu bütün chatlarda icazə verilir..:** `{i}`")
            except:
                pass
    else:
        await event.edit("**Bir istifadəçiyə cavab verin**")
    return await event.edit(
        f"**Qlobal olaraq admin edildi [{user.first_name}](tg://user?id={user.id})\n**{i} chat'da**"
    )


@register(outgoing=True, pattern="^.gdemote ?(.*)")
async def gdemote(event):
    event= event = event
    i = 0
    await event.get_sender()
    me = await event.client.get_me()
    await event.edit("`İcazə aşağı salınır...`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    f"@{me.username}" if me.username else my_mention
    await event.get_chat()
    if event.is_private:
        user = event.chat
        rank = event.pattern_match.group(1)
    else:
        event.chat.title
    try:
        user, rank = await get_full_user(event)
    except:
        pass
    if me == user:
        await event.edit("Öz icazəni aşağı sala bilmərsən")
        return
    try:
        if not rank:
            rank = "ㅤㅤ"
    except:
        return await event.edit("**Bir xəta baş verdi**")
    if user:
        telchanel = [
            d.entity.id
            for d in await event.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        rgt = ChatAdminRights(
            add_admins=None,
            invite_users=None,
            change_info=None,
            ban_users=None,
            delete_messages=None,
            pin_messages=None,
        )
        for x in telchanel:
            try:
                await event.client(EditAdminRequest(x, user, rgt, rank))
                i += 1
                await event.edit(f"**Admin olduğun qruplardan icazə aşağı salındır**: `{i}`")
            except:
                pass
    else:
        await event.edit(f"**Bir istifadəçiyə cavab verin**")
    return await event.edit(
        f"**Qlobal olaraq icazə aşağı salındı [{user.first_name}](tg://user?id={user.id})\n**{i} chat'da**"
    )

CmdHelp('gadmin').add_command(
  'gpromote', '<id/cavab>', 'İstifadəçini admin əlavə etmək səlahiyyətiniz olan bütün qruplarda admin edər').add_command(
  'gdemote', '<id/cavab>', 'İstifadəçinin admin hüquqlarını qlobal olaraq alar').add()
