from instagrapi import Client
from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag
import random
import string
from pathlib import Path
import json
import datetime
import re


# def freeze(self, message, days=0, hours=0):
#     self.is_logged = False
#     self.freeze_to = datetime.now() + datetime.timedelta(days=days, hours=hours)
#     freeze_to = re.search(r"(\d{4})\-(\d{2})\-(\d{2})", message)
#     if freeze_to:
#         year, month, day = map(int, freeze_to.groups())
#         self.freeze_to = datetime.now().replace(year=year, month=month, day=day)
#     self.freeze_at = datetime.now()
#     self.freeze_message = message
#     self.save(
#         update_fields=["is_logged", "freeze_to", "freeze_at", "freeze_message"]
#     )
#     return True


# def rebuild_client_settings(self, device=None):
#     self.client_settings = {}
#     self.build_client_settings(device)
#     self.login(relogin=True)
#     return self.client_settings


# def build_client_settings(self, device=None):
#     self.device = device
#     if not self.device:
#         self.device = Device.objects.order_by("id").first()
#     self.client_settings["device_settings"] = self.device.settings
#     self.client_settings["user_anget"] = self.device.build_user_agent(
#         self.locale or self.proxy.locale)
#     self.save(update_fields=["device", "client_settings"])
#     return self.client_settings


USERNAME = 'christianrpm90@gmail.com'
PASSWORD = 's3k111'
# nameFileSettings = USERNAME.replace("@", "").replace(".", "")

# file = Path('../uploads/'+nameFileSettings+'.json')
# if file.exists():
#     print(f"El archivo {nameFileSettings} existe.")
# else:
#     print(f"El archivo {nameFileSettings} no existe.")

print('PreLogin')
# cl = Client()
# cl.login(USERNAME, PASSWORD)
# with open('../uploads/christianrpm90.json', 'w') as f:
#     json.dump(cl.get_settings(), f, indent=2)

pathOne = Path(__file__).parent.parent
filenameOne = f".{pathOne}/uploads/christianrpm90.json"

print("Fecha Ini",datetime.datetime.now())

cl = Client(json.load(open(filenameOne)))
print('Logged')

print('downlad media')
media_pk = cl.media_pk_from_url('https://www.instagram.com/p/CmjhGdSqdRb/')
media_path = cl.photo_download(media_pk)

letters = string.ascii_lowercase
letters = ''.join(random.choice(letters) for i in range(10))
current_date_time = datetime.datetime.now()

print('upload photo')
cl.photo_upload(
    path=media_path,
    caption=letters
)
Path(media_path).unlink()
print("Fecha Fin",datetime.datetime.now())
# print(cl)
# print('Finished')

# print(newString)

# path = Path(__file__).parent.parent.parent
# filename = f'../uploads/{newString}.json'
# # print(path)
# # filename = f"{path}/uploads/{USERNAME}.json"
# with open(filename, 'w') as f:
#     json.dump({}, f, indent=2)

# print("Logging in...")
# cl = Client()
# if not exists("/tmp/dump.json"):  # first-time login
#     cl.set_device(device={...})
#     cl.set_uuids(uuids={...})
#     cl.login(user, password)
#     my_id = cl.user_id
#     fh.append_ids("cache/" + user + "_id", str(my_id))
# else:
#     settings = cl.load_settings(Path("/tmp/dump.json"))
#     print("Settings loaded successfully")
#     cl.login(user, password)
# cl.dump_settings(Path("/tmp/dump.json"))
# time.sleep(random.randint(10, 20) / 10)
# try:
#     cl.user_info(str(cl.user_id))
# except LoginRequired:
#     print(" *** re-login ***")
#     print(cl.username, cl.password)
#     cl.relogin()
#     print("Re-login executed.")
#     cl.dump_settings(Path("/tmp/dump.json"))
#     time.sleep(random.random()*3+0.4)
# time.sleep(random.random()+1.6)
# ig('scroll_feed')  # This calls cl.get_timeline_feed()
