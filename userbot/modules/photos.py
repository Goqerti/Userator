# U S Σ R Δ T O R / Coshgyn

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.events import register
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern="^.ascii ?(.*)")
async def asci(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Bir şəkilə cavab verin`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("`Bir şəkilə cavab verin`")
        return
    chat = "@asciiart_bot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("Real istifadəçilərə cavab olaraq istifadə edin.")
        return
    asc = await event.edit("**ASCII** `yaradılır...` 🔥")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=164766745)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.edit("@asciiart_bot'u `blokdan çıxardın və yenidən yoxlayın`")
            return
        if response.text.startswith("Forward"):
            await event.edit(
                "gizlilik ayarlarınızı düzəldin."
            )
        else:
            await event.delete()
            await event.client.send_file(
                event.chat_id,
                response.message.media,
                caption=f"@UseratorOT 🐍",
            )
            await event.client.send_read_acknowledge(conv.chat_id)


@register(outgoing=True, pattern="^.line ?(.*)")
async def line(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Bir şəkilə cavab verin`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("`Bir şəkilə cavab verin`")
        return
    chat = "@Lines50Bot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("Real istifadəçilərə cavab olaraq istifadə edin.")
        return
    asc = await event.edit("`Hazırlanır...` 🔥")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1120861844)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.edit("@Lines50Bot'u `blokdan çıxardın və yenidən yoxlayın`")
            return
        if response.text.startswith("Forward"):
            await event.edit(
                "gizlilik ayarlarınızı düzəldin."
            )
        else:
            await event.delete()
            await event.client.send_file(
                event.chat_id,
                response.message.media,
                caption=f"@UseratorOT 🐍",
            )
            await event.client.send_read_acknowledge(conv.chat_id)


@register(outgoing=True, pattern="^.colorize ?(.*)")
async def colorizer(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Bir şəkilə cavab verin`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("`Bir şəkilə cavab verin`")
        return
    chat = "@photocolorizerbot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("Real istifadəçilərə cavab olaraq istifadə edin.")
        return
    asc = await event.edit("`Foto rənglənir` 🔥")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1072675522)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.edit("@photocolorizerbot'u `blokdan çıxardın və yenidən yoxlayın`")
            return
        if response.text.startswith("Forward"):
            await event.edit(
                "gizlilik ayarlarınızı düzəldin."
            )
        else:
            await event.delete()
            await event.client.send_file(
                event.chat_id,
                response.message.media,
                caption=f"@UseratorOT 🐍",
            )
            await event.client.send_read_acknowledge(conv.chat_id)


@register(outgoing=True, pattern="^.pixel ?(.*)")
async def picture(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Bir şəkil/sticker'ə cavab verin`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("`Bir şəkil/sticker'ə cavab verin`")
        return
    chat = "@pixelatorbot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("Real istifadəçilərə cavab olaraq istifadə edin.")
        return
    asc = await event.edit("`Pixellənir...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=479711161)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.edit("@pixelatorBot'u `blokdan çıxardın və yenidən yoxlayın`")
            return
        if response.text.startswith("Forward"):
            await event.edit(
                "gizlilik ayarlarınızı düzəldin."
            )
        else:
            await event.delete()
            await event.client.send_file(
                event.chat_id,
                response.message.media,
                caption=f"@UseratorOT 🐍",
            )
            await event.client.send_read_acknowledge(conv.chat_id)


CmdHelp('photos').add_command(
    'ascii', None, 'Cavab verdiyiniz şəkilə ASCII effekti verər.'
).add_command(
    'line', None, 'Cavab verdiyiniz şəkilə 50Lines effekti verər.'
).add_command(
    'colorize', None, 'Ağ-qara şəkilləri rəngləndirər'
).add_command(
    'pixel', None, 'Cavab verdiyiniz şəkilə pixel effekti verər.'
).add()
