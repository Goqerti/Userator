# U S Σ R Δ T O R / Ümüd

import aria2p
from asyncio import sleep
from os import system
from userbot import LOGS, CMD_HELP
from userbot.events import register
from requests import get
from userbot.cmdhelp import CmdHelp

trackers_list = get(
    'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt'
).text.replace('\n\n', ',')
trackers = f"[{trackers_list}]"

cmd = f"aria2c \
--enable-rpc \
--rpc-listen-all=false \
--rpc-listen-port 6800 \
--max-connection-per-server=10 \
--rpc-max-request-size=1024M \
--seed-time=0.01 \
--max-upload-limit=5K \
--max-concurrent-downloads=5 \
--min-split-size=10M \
--follow-torrent=mem \
--split=10 \
--bt-tracker={trackers} \
--daemon=true \
--allow-overwrite=true"

aria2_is_running = system(cmd)

aria2 = aria2p.API(aria2p.Client(host="http://localhost", port=6800,
                                 secret=""))


@register(outgoing=True, pattern="^.amag(?: |$)(.*)")
async def magnet_download(event):
    magnet_uri = event.pattern_match.group(1)
    # 
    try:
        download = aria2.add_magnet(magnet_uri)
    except Exception as e:
        LOGS.info(str(e))
        await event.edit("Xəta:\n`" + str(e) + "`")
        return
    gid = download.gid
    await check_progress_for_dl(gid=gid, event=event, previous=None)
    await sleep(5)
    new_gid = await check_metadata(gid)
    await check_progress_for_dl(gid=new_gid, event=event, previous=None)


@register(outgoing=True, pattern="^.ator(?: |$)(.*)")
async def torrent_download(event):
    torrent_file_path = event.pattern_match.group(1)
    # 
    try:
        download = aria2.add_torrent(torrent_file_path,
                                     uris=None,
                                     options=None,
                                     position=None)
    except Exception as e:
        await event.edit(str(e))
        return
    gid = download.gid
    await check_progress_for_dl(gid=gid, event=event, previous=None)


@register(outgoing=True, pattern="^.aurl(?: |$)(.*)")
async def amagnet_download(event):
    uri = [event.pattern_match.group(1)]
    try:  # 
        download = aria2.add_uris(uri, options=None, position=None)
    except Exception as e:
        LOGS.info(str(e))
        await event.edit("Xəta :\n`{}`".format(str(e)))
        return
    gid = download.gid
    await check_progress_for_dl(gid=gid, event=event, previous=None)
    file = aria2.get_download(gid)
    if file.followed_by_ids:
        new_gid = await check_metadata(gid)
        await progress_status(gid=new_gid, event=event, previous=None)


@register(outgoing=True, pattern="^.aclear(?: |$)(.*)")
async def remove_all(event):
    await event.edit("`Davam edən endirmələr təmizlənir... `")
    try:
        removed = aria2.remove_all(force=True)
        aria2.purge_all()
    except:
        pass
    if not removed:  # .
        system("aria2p remove-all")
    await event.edit("`Bütün yüklənənlər uğurla təmizləndi.`")


@register(outgoing=True, pattern="^.apause(?: |$)(.*)")
async def pause_all(event):
    # Tüm devam eden indirmeleri duraklatır.
    await event.edit("`Endirmələr dayandırılır...`")
    aria2.pause_all(force=True)
    await event.edit("`Davam edən endirmələr uğurla dayandırıldı.`")


@register(outgoing=True, pattern="^.aresume(?: |$)(.*)")
async def resume_all(event):
    await event.edit("`Endirmələr davam etdirilir...`")
    aria2.resume_all()
    await event.edit("`Endirmələr davam etdirildi.`")
    await sleep(2.5)
    await event.delete()


@register(outgoing=True, pattern="^.ashow(?: |$)(.*)")
async def show_all(event):
    output = "output.txt"
    downloads = aria2.get_downloads()
    msg = ""
    for download in downloads:
        msg = msg + "Fayl: `" + str(download.name) + "`\nSürət: " + str(
            download.download_speed_string()) + "\nİşləm: " + str(
                download.progress_string()) + "\nToplam Həcmə: " + str(
                    download.total_length_string()) + "\nStatus: " + str(
                        download.status) + "\nTəxmini bitiş:  " + str(
                            download.eta_string()) + "\n\n"
    if len(msg) <= 4096:
        await event.edit("`Davam edən endirmələr: `\n" + msg)
        await sleep(5)
        await event.delete()
    else:
        await event.edit("`Çıxdı çox büyükdür, bu səbəbə görə fayl olaraq göndərilir...`")
        with open(output, 'w') as f:
            f.write(msg)
        await sleep(2)
        await event.delete()
        await event.client.send_file(
            event.chat_id,
            output,
            force_document=True,
            supports_streaming=False,
            allow_cache=False,
            reply_to=event.message.id,
        )


async def check_metadata(gid):
    file = aria2.get_download(gid)
    new_gid = file.followed_by_ids[0]
    LOGS.info("GID " + gid + " bu dəyərdən bu dəyərə dəyişdirilir:" + new_gid)
    return new_gid


async def check_progress_for_dl(gid, event, previous):
    complete = None
    while not complete:
        file = aria2.get_download(gid)
        complete = file.is_complete
        try:
            if not complete and not file.error_message:
                msg = f"\nEndirilen fayl: `{file.name}`"
                msg += f"\nSürət: {file.download_speed_string()}"
                msg += f"\nİşləm: {file.progress_string()}"
                msg += f"\nToplam Həcm: {file.total_length_string()}"
                msg += f"\nStatus: {file.status}"
                msg += f"\nTəxmini bitiş: {file.eta_string()}"
                if msg != previous:
                    await event.edit(msg)
                    msg = previous
            else:
                LOGS.info(str(file.error_message))
                await event.edit(f"`{msg}`")
            await sleep(5)
            await check_progress_for_dl(gid, event, previous)
            file = aria2.get_download(gid)
            complete = file.is_complete
            if complete:
                await event.edit(f"Fayl uğurla yükləndi: `{file.name}`"
                                 )
                return False
        except Exception as e:
            if " not found" in str(e) or "'file'" in str(e):
                await event.edit("Endirmə ləğv olundu :\n`{}`".format(file.name))
                await sleep(2.5)
                await event.delete()
                return
            elif " depth exceeded" in str(e):
                file.remove(force=True)
                await event.edit(
                    "Endirmə avtomatik olaraq ləğv edildi:\n`{}`\nTorrent ya da link xarabdır."
                    .format(file.name))

CmdHelp('aria').add_command(
    'aurl', 
    '[URL] (ya da) .amag [Magnet Linki] (ya da) .ator [torrent faylın yolu]', 
    'Bir faylı userbot serverinə endirər.'
    ).add_command(
        'apause', None, 'Davam edən endirməyi dayandırar ya da davam etdirər.'
    ).add_command(
        'aclear', None, 'Endirmə quyruğunu təmizləyər, davam edən bütün endirmələri silər.'
    ).add_command(
        'ashow', None, 'Davam edən endirmələrin statusunu göstərər.'
    ).add()
