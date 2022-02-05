import asyncio
from telethon import events
from userbot import UPBOT, BRAIN_CHECKER, WHITELIST
from userbot.events import register


@register(incoming=True, from_users=UPBOT, pattern="/ualive$")
@register(incoming=True, from_users=BRAIN_CHECKER, pattern="^.ualive$")
@register(incoming=True, from_users=WHITELIST, pattern="^.ualive$")
async def sudoers(s):
    await s.client.send_message(s.chat_id,f"**Bot işləyir ✅**\n`U S Σ R Δ T O R ✨` **versiya:** {DTO_VERSION}")
