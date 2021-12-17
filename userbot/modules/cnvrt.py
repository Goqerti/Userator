# U S Σ R Δ T O R / Coşqun

import asyncio
import os
import time
from datetime import datetime
from userbot.modules.upload_download import progress
from userbot import TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern="^.cnvrt (.*)")  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    if reply_message is None:
        await event.edit(
            "`Çevirmək üçün bir mediaya cavab verin`"
        )
        return
    await event.edit("__Media lokala yüklənilir...__")
    try:
        start = datetime.now()
        c_time = time.time()
        downloaded_file_name = await event.client.download_media(
            reply_message,
            TEMP_DOWNLOAD_DIRECTORY,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "__Yüklənilir...__")
            ),
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit(
            "`{}` 'a {} saniyədə yükləndi".format(downloaded_file_name, ms)
        )
        new_required_file_name = ""
        new_required_file_caption = ""
        command_to_run = []
        force_document = False
        voice_note = False
        supports_streaming = False
        if input_str == "ses":
            new_required_file_caption = "AUDIO" + str(round(time.time())) + ".ogg"
            new_required_file_name = (
                TEMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            )
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-map",
                "0:a",
                "-codec:a",
                "libopus",
                "-b:a",
                "100k",
                "-vbr",
                "on",
                new_required_file_name,
            ]
            voice_note = True
            supports_streaming = True
        elif input_str == "mp3":
            new_required_file_caption = "AUDIO" + str(round(time.time())) + ".mp3"
            new_required_file_name = (
                TEMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            )
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-vn",
                new_required_file_name,
            ]
            voice_note = False
            supports_streaming = True
        else:
            await event.edit("`Dsətəklənməyən tip`")
            os.remove(downloaded_file_name)
            return
        # TODO: re-write 😉
        process = await asyncio.create_subprocess_exec(
            *command_to_run,
           
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # subprocess sonlanır..
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
        os.remove(downloaded_file_name)
        if os.path.exists(new_required_file_name):
            end_two = datetime.now()
            await event.client.send_file(
                entity=event.chat_id,
                file=new_required_file_name,
                caption=f"@UseratorOT",
                allow_cache=False,
                silent=True,
                force_document=force_document,
                voice_note=voice_note,
                supports_streaming=supports_streaming,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "__Yüklənilir...__")
                ),
            )
            ms_two = (end_two - end).seconds
            os.remove(new_required_file_name)
            await event.edit(f"`{ms_two}` saniyədə mp3'ə çevrildi")

CmdHelp('cnvrt').add_command(
    'cnvrt', '<ses/mp3>', 'Cavab verdiyiniz səsi mp3ə mp3ü səsə videonu mp3 və ya səsə çevirər.'
).add()
