# U S Σ R Δ T O R / Ümüd
# duzune userator !

import os
import asyncio
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import DeletePhotosRequest, UploadProfilePhotoRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputPhoto
from userbot import TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp

PHOTO = TEMP_DOWNLOAD_DIRECTORY + "pp.jpg"
USERINFO= {}


@register(outgoing=True, pattern="^.klon(?: |$)(.*)")
async def klon(event):
    reply_message = event.reply_to_msg_id
    message = await event.get_reply_message()
    if reply_message:
        inp = message.sender.id
    else:
        inp = event.pattern_match.group(1)

    if not inp:
        await event.edit("`Bir istifadəçiyə cavab verin`")
        return

    await event.edit("`Klonlanır...`")

    try:
        user = await bot(GetFullUserRequest(inp))
    except ValueError:
        await event.edit("`Düzgün olmayan username!`")
        await asyncio.sleep(3)
        await event.delete()
        return
    me = await event.client.get_me()

    if USERINFO or os.path.exists(PHOTO):
        await event.edit("`Xəta baş verdi.`")
        await asyncio.sleep(2)
        await event.delete()
        return
    mne = await bot(GetFullUserRequest(me.id))
    USERINFO.update(
        {
            "first_name": mne.user.first_name or "",
            "last_name": mne.user.last_name or "",
            "about": mne.about or "",
        }
    )
    await bot(
        UpdateProfileRequest(
            first_name=user.user.first_name or "",
            last_name=user.user.last_name or "",
            about=user.about or "",
        )
    )
    if not user.profile_photo:
        await event.edit("`İstifadəçinin profil fotosu yoxdu, yalnız ad və bio'nu klonladım`")
        return
    await bot.download_profile_photo(user.user.id, PHOTO)
    await bot(
        UploadProfilePhotoRequest(file=await event.client.upload_file(PHOTO))
    )
    await event.edit("`Ahaha, Səni klonladım!`")


@register(outgoing=True, pattern="^.revert(?: |$)(.*)")
async def revert(event):
    if not (USERINFO or os.path.exists(PHOTO)):
        await event.edit("`Onsuz öz profilindəsən 🙄`")
        return
    if USERINFO:
        await bot(UpdateProfileRequest(**USERINFO))
        USERINFO.clear()
    if os.path.exists(PHOTO):
        me = await event.client.get_me()
        photo = (await bot.get_profile_photos(me.id, limit=1))[0]
        await bot(
            DeletePhotosRequest(
                id=[
                    InputPhoto(
                        id=photo.id,
                        access_hash=photo.access_hash,
                        file_reference=photo.file_reference,
                    )
                ]
            )
        )
        os.remove(PHOTO)
    await event.edit("`Hesab uğurla əvvəlki vəziyyətinə qaytarıldı!`")


CmdHelp('klon').add_command(
    'klon',  None, 'Seçdiyiniz istifadəçini klonlayar'
).add_command(
    'revert',  None, 'Əvvəlki vəziyyətinə döndərər.'
).add()
