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
from instagrapi.exceptions import (
    TwoFactorRequired,
    ChallengeRequired,
    ClientLoginRequired,
    ClientError
)


class InstagrapiService():
    @classmethod
    def setParameters(self, request):
        req = request.json
        pathFile = self.saveFiles(request, req['file'])
        data = {
            'account': req['account'],
            'password': req.get('password') or '',
            'description': req.get('description') or '',
            'md5': req.get('md5') or '',
            'file': pathFile,
            'font': req.get('font') or 'Roboto-Bold',
            'fontSize': req.get('fontSize') or 56,
            'color_text': req.get('color_text') or '#000000',
            'background_color_text': req.get('background_color_text') or '#FFFFFF',
            'title': req.get('title') or '',
            'link': req.get('link') or '',
            'shortcut_link': req.get('shortcut_link') or '',
            'price': req.get('price') or '',
        }
        self.validateFields(data)
        return data

    @classmethod
    def setParametersLogin(self, request):
        req = self.validateFieldsLogin(request.json)
        data = {
            'account': req['account'],
            'password': req.get('password') or '',
            'md5': req.get('md5') or '',
        }
        return data

    @classmethod
    def isLogin(self, obj):
        user = User.findUser(obj['account'], obj['md5'])
        cl = Client()
        if len(user) == 0:
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

    @classmethod
    def saveSessionOrNewLogin(self, obj, cl):
        if not obj.get("password"):
            raise ValueError(
                "El campo password es obligatorio para un nuevo inicio de sesion")
        cl = self.login(obj)
        userObj = {
            'account_ig': obj['account'],
            'cookie': json.dumps(cl.get_settings()),
            'md5': obj['md5']
        }
        userObj = User.createOrUpdateUser(userObj)
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
        except ChallengeRequired as e:
            raise ValueError(
                "Error: Se requiere resolver una capa de seguridad. Por favor, completa el desafío en la aplicación de Instagram o en el sitio web.")
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
            color_text=obj['color_text'],
            background_color_text=obj['background_color_text']
        )
        try:
            cl = self.isLogin(obj)
            cl.video_upload_to_story(
                path=buildout.path,
                stickers=buildout.stickers
            )
        except ClientLoginRequired as e:
            raise ValueError(f"Error: {e}")
        except (ChallengeRequired, ClientError) as e:
            raise ValueError(
                "Error: Se requiere resolver una capa de seguridad. Por favor, completa el desafío en la aplicación de Instagram o en el sitio web.")
        except Exception as e:
            raise ValueError(f"Error inesperado: {e}")
        Path(mediapath).unlink()
        Path(backgroundFile).unlink()

    @classmethod
    def searchFont(self, search):
        return TextClip.search(search, 'font')

    @classmethod
    def validateFields(self, obj):
        if not obj.get("account"):
            raise ValueError("El campo account es obligatorio")
        if not obj.get("md5"):
            raise ValueError("El campo md5 es obligatorio")
        if not (self.validateColorHexadecimal(obj['color_text']) and self.validateColorHexadecimal(obj['background_color_text'])):
            raise ValueError(
                "Los campos color_text y background_color_text al menos uno de estos colores ingresados es inválido.")
        return obj

    @classmethod
    def validateFieldsLogin(self, obj):
        if not obj.get("account"):
            raise ValueError("El campo account es obligatorio")
        if not obj.get("md5"):
            raise ValueError("El campo md5 es obligatorio")
        if not obj.get("password"):
            raise ValueError("El campo password es obligatorio")
        return obj

    @classmethod
    def validateColorHexadecimal(self, color):
        patron = re.compile(r'^#(?:[0-9a-fA-F]{3}){1,2}$')
        return bool(patron.match(color))

    @classmethod
    def saveFiles(self, request, file):
        randomName = ''.join(random.choice(string.ascii_lowercase)
                             for i in range(10))
        extension = "jpeg"
        path = Path(__file__).parent.parent
        filename = f"{path}/uploads/{randomName}.{extension}"
        response = requests.get(file)
        with open(filename, "wb") as f:
            f.write(response.content)
        return filename

    @classmethod
    def loginInstagramTmp(self, obj):
        cl = Client()
        cl = self.login(obj)
        userObj = {
            'account_ig': obj['account'],
            'cookie': json.dumps(cl.get_settings()),
            'md5': obj['md5']
        }
        User.createOrUpdateUser(userObj)
        return User.findUser(obj['account'], obj['md5'])

    @classmethod
    def login(self, obj):
        try:
            cl = Client()
            cl.login(obj['account'], obj['password'])
        except ClientLoginRequired as e:
            raise ValueError(f"Error: {e}")
        except (ChallengeRequired, ClientError) as e:
            raise ValueError(
                "Error: Se requiere resolver una capa de seguridad. Por favor, completa el desafío en la aplicación de Instagram o en el sitio web.")
        except Exception as e:
            raise ValueError(f"Error inesperado: {e}")
        return cl
