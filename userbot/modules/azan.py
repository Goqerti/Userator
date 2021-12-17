# U S Σ R Δ T O R / Ümüd

import json

import requests

from userbot.cmdhelp import CmdHelp
from userbot.events import register

PLACE = ""


@register(outgoing=True, pattern=r"^\.azan (.*)")
async def get_adzan(adzan):
    await adzan.edit("Gözləyin 🕋")
    if not adzan.pattern_match.group(1):
        LOCATION = PLACE
        if not LOCATION:
            await adzan.edit("`Xaiş bir şəhər adı yazın.`")
            return
    else:
        LOCATION = adzan.pattern_match.group(1)

    # url = f'http://muslimsalat.com/{LOKASI}.json?key=bd099c5825cbedb9aa934e255a81a5fc'
    url = f"https://api.pray.zone/v2/times/today.json?city={LOCATION}"
    request = requests.get(url)
    if request.status_code == 500:
        return await adzan.edit(f"Axtardığınız sorğu yalnışdır : `{LOCATION}`")

    parsed = json.loads(request.text)

    city = parsed["results"]["location"]["city"]
    country = parsed["results"]["location"]["country"]
    timezone = parsed["results"]["location"]["timezone"]
    date = parsed["results"]["datetime"][0]["date"]["gregorian"]

    imsak = parsed["results"]["datetime"][0]["times"]["Imsak"]
    subuh = parsed["results"]["datetime"][0]["times"]["Fajr"]
    zuhur = parsed["results"]["datetime"][0]["times"]["Dhuhr"]
    ashar = parsed["results"]["datetime"][0]["times"]["Asr"]
    maghrib = parsed["results"]["datetime"][0]["times"]["Maghrib"]
    isya = parsed["results"]["datetime"][0]["times"]["Isha"]

    result = (
        f"**Namaz vaxtları :**\n\n"
        f"📅 **{date} **\n"
        f"🌏 __{city}__\n\n"
        f"**İmsak //** `{imsak}`\n"
        f"**Sübh //** `{subuh}`\n"
        f"**Zöhr //** `{zuhur}`\n"
        f"**Əsr //** `{ashar}`\n"
        f"**Məğrib //** `{maghrib}`\n"
        f"**İşa //** `{isya}`\n"
    )

    await adzan.edit(result)


Help = CmdHelp('azan')
Help.add_command('azan şəhər adı',  None, 'Namaz vaxtlarını göstərər').add()
