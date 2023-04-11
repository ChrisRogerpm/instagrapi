from instagrapi import Client
from utils.storyCustom import StoryBuilder
from utils.ImageColor import ImageColor
from moviepy.editor import TextClip
from flask import jsonify
from models.User import User
from pathlib import Path
import json
import requests
import string
import random
from datetime import datetime
import pytz
import re


class InstagrapiService():
    @classmethod
    def setParameters(self, request):
        req = self.validateFields(request.json)
        pathFile = self.saveFiles(request, req['file'],  False)
        data = {
            'account': req['account'],
            'password': req.get('password') or '',
            'description': req.get('description') or '',
            'md5': req.get('md5') or '',
            'file': pathFile,
            # 'font': req.get('font') or 'DejaVu-Sans-Bold',
            'font': req.get('font') or 'Roboto-Bold',
            'fontSize': req.get('fontSize') or 56,
            'colorLabel': req.get('colorLabel') or '#000000',
            'backgroundLabel': req.get('backgroundLabel') or '#FFFFFF',
            'title': req.get('title') or '',
            'link': req.get('link') or '',
            'shortcut_link': req.get('shortcut_link') or '',
            'price': req.get('price') or '',
        }
        return data

    @classmethod
    def isLogin(self, obj):
        try:
            user = User.findUser(obj['md5'])
            cl = Client()
            if len(user) == 0:
                print('User not found')
                cl = self.saveSessionOrNewLogin(obj, cl)
            else:
                tz = pytz.timezone('America/Montevideo')
                dateExpired = user['dateExpired'].strftime("%Y-%m-%d")
                nowDate = datetime.now(tz).strftime("%Y-%m-%d")
                if dateExpired == nowDate:
                    cl = self.saveSessionOrNewLogin(obj, cl)
                else:
                    cookie = json.loads(user['cookie'])
                    cl = Client(cookie)
            return cl
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def saveSessionOrNewLogin(self, obj, cl):
        if not obj.get("password"):
            raise ValueError(
                "El campo password es obligatorio para una nuevo login o un re login")
        cl.login(obj['account'], obj['password'])
        userObj = {
            'account_ig': obj['account'],
            'cookie': json.dumps(cl.get_settings()),
            'md5': obj['md5']
        }
        User.createOrUpdateUser(userObj)
        return cl

    @classmethod
    def uploadPhoto(self, obj):
        mediapath = obj['file']
        try:
            cl = self.isLogin(obj)
            cl.photo_upload(
                path=Path(mediapath),
                caption=obj['description'],
            )
            Path(mediapath).unlink()
        except (Exception, ValueError) as ex:
            self.catchs_exception(ex, obj)
        # cl = self.isLogin(obj)
        # cl.photo_upload(
        #     path=Path(mediapath),
        #     caption=obj['description'],
        # )
        # Path(mediapath).unlink()

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
        backgroundColor = ImageColor.getColorBackgroundImage(mediapath)
        backgroundFile = ImageColor.makeImageBackground(backgroundColor)
        buildout = StoryBuilder(
            path=mediapath,
            bgpath=backgroundFile,
            font=obj['font'],
            fontsize=obj['fontSize']
        ).makeClipMedia(
            link=obj['link'],
            title=obj['title'],
            price=obj['price'],
            shortcut_link=obj['shortcut_link'],
            colorLabel=obj['colorLabel'],
            backgroundLabel=obj['backgroundLabel']
        )
        try:
            cl = self.isLogin(obj)
            cl.video_upload_to_story(
                path=buildout.path,
                stickers=buildout.stickers
            )
            Path(mediapath).unlink()
            Path(backgroundFile).unlink()
        except (Exception, ValueError) as ex:
            self.catchs_exception(ex, obj)

    @classmethod
    def catchs_exception(self, ex, obj):
        data = str(ex)
        if(bool(re.compile("login_required").search(data))):
            self.reLogin(obj)
            raise ValueError("Se ha iniciado sesión nuevamente")
        raise ValueError(data)

    @classmethod
    def reLogin(self, obj):
        try:
            cl = Client()
            cl = self.saveSessionOrNewLogin(obj, cl)
        except(Exception) as ex:
            raise ValueError(str(ex))
        return cl

    @classmethod
    def searchFont(self, search):
        return TextClip.search(search, 'font')

    @classmethod
    def validateFields(self, obj):
        if not obj.get("account") or not obj.get("md5"):
            raise ValueError("Los campos account y md5 son obligatorios")
        if not (self.validateColorHexadecimal(obj['colorLabel']) and self.validateColorHexadecimal(obj['backgroundLabel'])):
            raise ValueError(
                "Los campos colorLabel y backgroundLabel al menos uno de estos colores ingresados es inválido.")
        return obj

    @classmethod
    def validateColorHexadecimal(self, color):
        # Expresión regular para validar colores hexadecimales de 3 o 6 dígitos
        patron = re.compile(r'^#(?:[0-9a-fA-F]{3}){1,2}$')
        return bool(patron.match(color))

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
