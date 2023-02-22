from instagrapi import Client
from instagrapi.types import StoryLink, StorySticker, StoryStickerLink, StoryBuild
from utils.storyCustom import StoryBuilder
# from instagrapi.story import StoryBuilder
from pathlib import Path
from moviepy.editor import VideoFileClip, TextClip
import json
import requests
import string
import random


class InstagrapiService():
    @classmethod
    def setParameters(self, request):
        req = self.validateFields(request.json)
        pathFile = self.saveFiles(request, req['file'],  False)
        # pathBackground = self.saveFiles(request, file['background'], True)
        data = {
            'account': req['account'],
            'password': req['password'],
            'description': req.get('description') or '',
            'file': pathFile,
            # 'background': pathBackground,
            'font': req.get('font') or 'Roboto',
            'fontSize': req.get('fontSize') or 48,
            'color': req.get('color') or 'black',
            'title': req.get('title') or '',
            'link': req.get('link') or '',
            'shortcut_link': req.get('shortcut_link') or '',
            'price': req.get('price') or '',
        }
        return data

    @classmethod
    def isLogin(self, obj):
        try:
            fileCookie = obj['account'].replace("@", "").replace(".", "")
            dirPath = Path(__file__).parent.parent
            filePath = f"{dirPath}/uploads/{fileCookie}.json"
            file = Path(filePath)
            cl = Client()
            if file.exists():
                # print(f"El archivo {fileCookie} existe.")
                cl = Client(json.load(open(filePath)))
            # else:
            #     print(f"El archivo {fileCookie} no existe.")
                cl.login(obj['account'], obj['password'])
                with open(filePath, 'w') as f:
                    json.dump(cl.get_settings(), f, indent=2)
            return cl
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def uploadPhoto(self, obj):
        mediapath = obj['file']

        cl = self.isLogin(obj)
        cl.photo_upload(
            path=Path(mediapath),
            caption=obj['description'],
        )
        Path(mediapath).unlink()

    @classmethod
    def uploadVideo(self, obj):
        mediapath = obj['file']

        cl = self.isLogin(obj)
        cl.video_upload(
            path=Path(mediapath),
            caption=obj['description'],
        )
        Path(mediapath).unlink()

    @classmethod
    def uploadStoryPhotoVideo(self, obj):
        mediapath = obj['file']
        buildout = StoryBuilder(
            path=mediapath,
            bgpath=None,  # if obj['background'] == '' else obj['background'],
            color=obj['color'],
            font=obj['font'],
            fontsize=obj['fontSize']
        ).makeClipMedia(
            link=obj['link'],
            title=obj['title'],
            price=obj['price'],
            shortcut_link=obj['shortcut_link'],
        )
        cl = self.isLogin(obj)
        cl.video_upload_to_story(
            path=buildout.path,
            stickers=buildout.stickers
        )
        Path(mediapath).unlink()

    @classmethod
    def searchFont(self, search):
        return TextClip.search(search, 'font')

    @classmethod
    def validateFields(self, obj):
        if obj['account'] == '' or obj['password'] == '':
            raise ValueError("Los campos account y password son obligatorios")
        return obj

    @classmethod
    def saveFiles(self, request, file, isBackground):
        randomName = ''.join(random.choice(string.ascii_lowercase)
                             for i in range(10))
        extension = "jpeg"  # re.search("\.([^.]+)$", file).group(1)

        path = Path(__file__).parent.parent
        filename = f"{path}/uploads/{randomName}.{extension}"

        response = requests.get(file)
        with open(filename, "wb") as f:
            f.write(response.content)
        return filename

    @classmethod
    def saveCookieSession(self):
        data = [{"a": 54, "b": 87}, {"c": 81, "d": 63}, {"e": 17, "f": 39}]
        letters = string.ascii_lowercase
        letters = ''.join(random.choice(letters) for i in range(10))
        # print ( ''.join(random.choice(letters) for i in range(10)) )
        with open(f"uploads/{letters}.json", 'w') as f:
            json.dump(data, f, indent=2)
