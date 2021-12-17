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

''' AntiSpamBot '''

from asyncio import sleep
from requests import get

from telethon.events import ChatAction
from telethon.tl.types import ChannelParticipantsAdmins, Message

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, ANTI_SPAMBOT, ANTI_SPAMBOT_SHOUT, bot


@bot.on(ChatAction)
async def anti_spambot(welcm):
    try:
        ''' AntiSpam '''
        if not ANTI_SPAMBOT:
            return
        if welcm.user_joined or welcm.user_added:
            adder = None
            ignore = False
            users = None

            if welcm.user_added:
                ignore = False
                try:
                    adder = welcm.action_message.from_id
                except AttributeError:
                    return

            async for admin in bot.iter_participants(
                    welcm.chat_id, filter=ChannelParticipantsAdmins):
                if admin.id == adder:
                    ignore = True
                    break

            if ignore:
                return

            elif welcm.user_joined:
                users_list = hasattr(welcm.action_message.action, "users")
                if users_list:
                    users = welcm.action_message.action.users
                else:
                    users = [welcm.action_message.from_id]

            await sleep(5)
            spambot = False

            if not users:
                return

            for user_id in users:
                async for message in bot.iter_messages(welcm.chat_id,
                                                       from_user=user_id):

                    correct_type = isinstance(message, Message)
                    if not message or not correct_type:
                        break

                    join_time = welcm.action_message.date
                    message_date = message.date

                    if message_date < join_time:
                        # 
                        continue

                    check_user = await welcm.client.get_entity(user_id)

                    # . ###
                    print(
                        f"Qatılan istifadəçi: {check_user.first_name} [ID: {check_user.id}]"
                    )
                    print(f"Söhbət: {welcm.chat.title}")
                    print(f"Zaman: {join_time}")
                    print(
                        f"Göndərdiyi mesaj: {message.text}\n\n[Zaman: {message_date}]"
                    )
                    ##############################################

                    try:
                        cas_url = f"https://combot.org/api/cas/check?user_id={check_user.id}"
                        r = get(cas_url, timeout=3)
                        data = r.json()
                    except BaseException:
                        print(
                            "CAS yoxlanışı uğursuzdur, köhnə anti_spambot yoxlanışına dönülür."
                        )
                        data = None
                        pass

                    if data and data['ok']:
                        reason = f"[Combot Anti Spam tərəfindən banlandı.](https://combot.org/cas/query?u={check_user.id})"
                        spambot = True
                    elif "t.cn/" in message.text:
                        reason = "`t.cn` URL'ləri görsəndi."
                        spambot = True
                    elif "t.me/joinchat" in message.text:
                        reason = "Potansiyel reklam mesajı"
                        spambot = True
                    elif message.fwd_from:
                        reason = "Başqasından yönləndirilən mesaj"
                        spambot = True
                    elif "?start=" in message.text:
                        reason = "Telegram botu `start` linki"
                        spambot = True
                    elif "bit.ly/" in message.text:
                        reason = "`bit.ly` URL'ləri tapıldı."
                        spambot = True
                    else:
                        if check_user.first_name in ("Bitmex", "Promotion",
                                                     "Information", "Dex",
                                                     "Announcements", "Info",
                                                     "Məlumat", "Məlumat"
                                                     "Məlumatlandırma", "Məlumatlandırmalar"):
                            if check_user.last_name == "Bot":
                                reason = "BilinƏn SpamBot"
                                spambot = True

                    if spambot:
                        print(f"Potansiyel Spam Mesajı: {message.text}")
                        await message.delete()
                        break

                    continue  # 

            if spambot:
                chat = await welcm.get_chat()
                admin = chat.admin_rights
                creator = chat.creator
                if not admin and not creator:
                    if ANTI_SPAMBOT_SHOUT:
                        await welcm.reply(
                            "@admins\n"
                            "`ANTI SPAMBOT TAPILDI!\n"
                            "BU İSTİFADƏÇİ MƏNİM SPAMBOT ALQORİTİMLƏ UYĞUNLAŞIR!`"
                            f"SƏBƏB: {reason}")
                        kicked = False
                        reported = True
                else:
                    try:

                        await welcm.reply(
                            "`Potansiyel Spambot Tapıldı !!`\n"
                            f"`SƏBƏB:` {reason}\n"
                            "İndilik qrupdan atılır, bu ID irəlidəki vaxtlar üçün qeyd ediləcək.\n"
                            f"`İSTİFADECİ:` [{check_user.first_name}](tg://user?id={check_user.id})"
                        )

                        await welcm.client.kick_participant(
                            welcm.chat_id, check_user.id)
                        kicked = True
                        reported = False

                    except BaseException:
                        if ANTI_SPAMBOT_SHOUT:
                            await welcm.reply(
                                "@admins\n"
                                "`ANTI SPAMBOT TAPILDI!\n"
                                "BU İSTİFADƏÇİ MƏNİM SPAMBOT ALQORİTİMLƏ UYĞUNLAŞIR`"
                                f"SƏBƏB: {reason}")
                            kicked = False
                            reported = True

                if BOTLOG:
                    if kicked or reported:
                        await welcm.client.send_message(
                            BOTLOG_CHATID, "#ANTI_SPAMBOT SİKAYET\n"
                            f"İSTİFADECİ: [{check_user.first_name}](tg://user?id={check_user.id})\n"
                            f"İstifadəçi IDsi: `{check_user.id}`\n"
                            f"Söhbət: {welcm.chat.title}\n"
                            f"Söhbət IDsi: `{welcm.chat_id}`\n"
                            f"Səbəb: {reason}\n"
                            f"Mesaj:\n\n{message.text}")
    except ValueError:
        pass


CMD_HELP.update({
    'anti_spambot':
    "İşlədilişi: Bu modul config.env faylında ya da env dəyəri ilə aktivləşdirilibsə,\
        \nəgər bu spamcılar DTÖUserBot'un anti-spam alqoritimi ilə uyğunlaşırsa, \
        \nbu modul qrupdakı spamcıları qrupdan banlayar (ya da adminlərə məlumat verər)."
})
