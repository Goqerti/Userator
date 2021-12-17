# Copyright (C) 2020 U S Σ R Δ T O R
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# credits for FridayOT
# port/edit Coshgyn

import os, subprocess
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from userbot import TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.cmdhelp import CmdHelp

thumb_image_path =(TEMP_DOWNLOAD_DIRECTORY) + "/thumb_image.jpg"


def get_video_thumb(file, output=None, width=320):
    output = file + ".jpg"
    metadata = extractMetadata(createParser(file))
    p = subprocess.Popen(
        [
            "ffmpeg",
            "-i",
            file,
            "-ss",
            str(
                int((0, metadata.get("duration").seconds)[metadata.has("duration")] / 2)
            ),
            # '-filter:v', 'scale={}:-1'.format(width),
            "-vframes",
            "1",
            output,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    p.communicate()
    if not p.returncode and os.path.lexists(file):
        os.remove(file)
        return output


@register(outgoing=True, pattern="^.savethumbnail")
async def _(event):
    if event.fwd_from:
        return
    await event.edit("`Hazırlanır...`")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        downloaded_file_name = await event.client.download_media(
            await event.get_reply_message(), TEMP_DOWNLOAD_DIRECTORY
        )
        if downloaded_file_name.endswith(".mp4"):
            downloaded_file_name = get_video_thumb(downloaded_file_name)
        metadata = extractMetadata(createParser(downloaded_file_name))
        height = 0
        if metadata.has("height"):
            height = metadata.get("height")
   
        Image.open(downloaded_file_name).convert("RGB").save(downloaded_file_name)
        img = Image.open(downloaded_file_name)
     
        img.resize((320, height))
        img.save(thumb_image_path, "JPEG")

        os.remove(downloaded_file_name)
        await event.edit(
            "Verdiyiniz şəkil/videonun thumbnail'i yüklənildi. "
            + "Bu thumbnail'i `.getthumbnail` əmri ilə çağıra bilərsiniz."
        )
    else:
        await event.edit("thumbnail kimi saxlamaq istədiyiniz şəkil/videoya cavab verin")


@register(outgoing=True, pattern="^.clearthumbnail")
async def _(event):
    if event.fwd_from:
        return
    if os.path.exists(thumb_image_path):
        os.remove(thumb_image_path)
    await event.edit("**Seçdiyiniz thumbnail silindi**")


@register(outgoing=True, pattern="^.getthumbnail")
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        try:
            a = await event.client.download_media(
                r.media.document.thumbs[0], TEMP_DOWNLOAD_DIRECTORY
            )
        except Exception as e:
            await event.edit(str(e))
        try:
            await event.client.send_file(
                event.chat_id,
                a,
                force_document=False,
                allow_cache=False,
                reply_to=event.reply_to_msg_id,
            )
            os.remove(a)
            await event.delete()
        except Exception as e:
            await event.edit(str(e))
    elif os.path.exists(thumb_image_path):
        caption_str = "**Hazırki thumbnail**\n `.clearthumbnail` əmri iləsilə bilərsiniz"
        await event.client.send_file(
            event.chat_id,
            thumb_image_path,
            caption=caption_str,
            force_document=False,
            allow_cache=False,
            reply_to=event.message.id,
        )
        await event.edit(caption_str)
    else:
        await event.edit("`.getthumbnail` yazaraq thumbnaili çağıra bilərsiniz")

CmdHelp('thumbnail').add_command('savethumbnail', None, 'Cavab verdiyiniz şəkil/videonu thumbnail kimi saxlayar').add_command('clearthumbnail', None, 'Mövcud thumbnaili silər').add_command('getthumbnail', None, 'Hazırki thumbnaili çağırar').add_info('`İstifadə üçün BOTLOG lazım deyildir`').add()
