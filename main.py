import os
from pyrogram import Client


BOT_TOKEN = os.environ.get('BOT_TOKEN',
                           '6183397097:AAETlxAm8ZTFSCHZzMCAI9aECwBURe455Fk')

plugins = dict(root="plugins")
API_ID = 16514976
API_HASH = '40bd8634b3836468bb2fb7eafe39d81a'


app = Client("Forwardbot",
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             plugins=plugins,
             workers=5)



# os.system("clear")
print("Started :)")
app.run()
