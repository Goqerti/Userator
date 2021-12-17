# U S Σ R Δ T O R / Ümüd

import asyncio
import io, os, math
from io import BytesIO
import numpy as np
from pydub import AudioSegment
from telethon import types
from userbot.events import register
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, pattern="^.bass ?(.*)")
async def bassbooster(e):
    v = False
    accentuate_db = 40
    reply = await e.get_reply_message()
    if not reply:
        await e.edit("**Bir səsli mediaya cavab verin**")
        return
    if e.pattern_match.group(1):
        ar = e.pattern_match.group(1)
        try:
            int(ar)
            if int(ar) >= 2 and int(ar) <= 100:
                accentuate_db = int(ar)
            else:
                await e.edit("**BassBost** `səviyyəsi 2-100 arası olmalıdır.`")
                return
        except Exception as exx:
            await e.edit("`Bir xəta baş verdi` \n**Xəta:** " + str(exx))
            return
    else:
        accentuate_db = 2
    await e.edit("`Fayl yüklənilir...`")
    fname = await e.client.download_media(message=reply.media)
    await e.edit("`Bass effekti hazırlanır...`")
    if fname.endswith(".oga") or fname.endswith(".ogg"):
        v = True
        audio = AudioSegment.from_file(fname)
    elif fname.endswith(".mp3") or fname.endswith(".m4a") or fname.endswith(".wav"):
        audio = AudioSegment.from_file(fname)
    else:
        await e.edit(
            "`Dəstəklənməyən fayl tipi` \n**Hazırda dəstəklənən fayl tipləri :** `mp3, m4a, wav.`"
        )
        os.remove(fname)
        return
    sample_track = list(audio.get_array_of_samples())
    await asyncio.sleep(0.3)
    est_mean = np.mean(sample_track)
    await asyncio.sleep(0.3)
    est_std = 3 * np.std(sample_track) / (math.sqrt(2))
    await asyncio.sleep(0.3)
    bass_factor = int(round((est_std - est_mean) * 0.005))
    await asyncio.sleep(5)
    attenuate_db = 0
    filtered = audio.low_pass_filter(bass_factor)
    await asyncio.sleep(5)
    out = (audio - attenuate_db).overlay(filtered + accentuate_db)
    await asyncio.sleep(6)
    m = io.BytesIO()
    if v:
        m.name = "voice.ogg"
        out.split_to_mono()
        await e.edit("`Hazırlanır...`")
        await asyncio.sleep(0.3)
        out.export(m, format="ogg", bitrate="64k", codec="libopus")
        await e.edit("`Effekt hazırlandı\n Fayl göndərilir...`")
        await e.client.send_file(
            e.to_id,
            m,
            reply_to=reply.id,
            voice_note=True,
            caption="[U S Σ R Δ T O R](t.me/UseratorOT) `ilə bass gücləndirildi`",
        )

    else:
        m.name = "UseratorBASS.mp3"
        await e.edit("`Hazırlanır...`")
        await asyncio.sleep(0.3)
        out.export(m, format="mp3")
        await e.edit("`Effekt hazırlandı\n Fayl göndərilir...`")
        await e.client.send_file(
            e.to_id,
            m,
            reply_to=reply.id,
            attributes=[
                types.DocumentAttributeAudio(
                    duration=reply.document.attributes[0].duration,
                    title=f"BassBoost {str(accentuate_db)}lvl",
                    performer="BassBoost",
                )
            ],
            caption="[U S Σ R Δ T O R](t.me/UseratorOT) `ilə bass gücləndirildi`",
        )
    await e.delete()
    os.remove(fname)
    
CmdHelp('bass').add_command('bass', '<1-100>', 'Cavab verdiyiniz səs faylına bass effekti verər').add()
