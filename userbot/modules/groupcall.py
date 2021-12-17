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

from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc
from userbot.events import register
from userbot import bot, get_call
from userbot.cmdhelp import CmdHelp


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]

@register(pattern="^.startvc$", groups_only=True)
async def _(e):
    chat = await e.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        await e.edit("admin deyilsən")
        return
    try:
        await e.client(startvc(e.chat_id))
        await e.edit("`Səsli zəng başladıldı`")
    except Exception as ex:
        await e.edit(f"Xəta: `{ex}`")

@register(outgoing=True, pattern="^.stopvc", groups_only=True)
async def _(e):
    chat = await e.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        await e.edit("Admin deyilsən")
        return
    try:
        await e.client(stopvc(await get_call(e)))
        await e.edit("`Qrup zəngi dayandırıldı`")
    except Exception as ex:
        await e.edit(f"Xəta: `{ex}`")



@register(outgoing=True, pattern="^.vctag", groups_only=True,)
async def _(e):
    await e.edit("`İstifadəçilər səsli zəngə çağrılır...`")
    users = []
    z = 0
    async for x in e.client.iter_participants(e.chat_id):
        if not x.bot:
            users.append(x.id)
    hmm = list(user_list(users, 6))
    for p in hmm:
        try:
            await e.client(invitetovc(call=await get_call(e), users=p))
            z += 6
        except BaseException:
            pass
    await e.edit(f"`{z} istifadəçi çağırıldı`")

CmdHelp('groupcall').add_command('startvc' , None, 'Səsli söhbət başladar').add_command('stopvc', None, 'Səsli söhbəti dayandırar').add_command('vctag', None, 'İnsanları səsli söhbətə dəvət edər').add()
