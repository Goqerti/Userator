from telethon.sync import TelegramClient
from telethon.sessions import StringSession

print("""Hazır dəyərlər yoxdursa, my.telegram.org
daxil olub app yaradın.""")

API_KEY = input("API ID: ")
API_HASH = input("API HASH: ")
with TelegramClient(StringSession(), API_KEY, API_HASH) as client:
    session_string = client.session.save()
    saved_messages_template = """<code>STRING_SESSION</code>: <code>{}</code>
️<i>@UseratorOT</i>""".format(session_string)
    client.send_message("me", saved_messages_template, parse_mode="html")
    print("StringSession kayıtlı mesajlara göndərildi.")
