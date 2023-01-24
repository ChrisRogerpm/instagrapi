from instagrapi import Client
from instagrapi.types import StoryLink, StorySticker, StoryStickerLink, StoryBuild
from utils.storyCustom import StoryBuilder
# from instagrapi.story import StoryBuilder
from pathlib import Path
from moviepy.editor import VideoFileClip, TextClip


class InstagrapiService():
    @classmethod
    def setParameters(self, request):
        file = request.files
        req = self.validateFields(request.form)

        pathFile = self.saveFiles(request, file['file'],  False)
        pathBackground = self.saveFiles(request, file['background'], True)

        data = {
            'account': req['account'],
            'password': req['password'],
            'description': req.get('description') or '',
            'file': pathFile,
            'background': pathBackground,
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
            cl = Client()
            cl.login(obj['account'], obj['password'])
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
        print(type(obj['color']))
        buildout = StoryBuilder(
            path=mediapath,
            bgpath=None if obj['background'] == '' else obj['background'],
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
        pathUrl = request.path
        extFile = ''
        if isBackground:
            return ''
        if file.filename == '':
            raise ValueError("El campo file es obligatorio")

        if pathUrl.endswith('uploadStoryPhotoVideo'):
            acceptedExtensions = ["mp4", "jpeg"]
            extFile = 'mp4' if file.content_type.endswith('mp4') else 'jpeg'
            if extFile not in acceptedExtensions:
                raise ValueError(
                    "El archivo no es un formato admitido, solo se acepta archivos jpeg y mp4")
        elif pathUrl.endswith('Video'):
            extFile = 'mp4' if file.content_type.endswith('mp4') else 'jpeg'
            if extFile != 'mp4':
                raise ValueError(
                    "El archivo no es un formato admitido, solo se acepta archivos mp4")
        else:
            extFile = 'mp4' if file.content_type.endswith('mp4') else 'jpeg'
            if extFile != 'jpeg':
                raise ValueError(
                    "El archivo no es un formato admitido, solo se acepta archivos jpeg")

        path = Path(__file__).parent.parent
        filename = f"{path}/uploads/{file.filename}"
        file.save(filename)

        # file_path = Path(filename)
        # if file_path.suffix != f".{extFile}":
        #     Path(filename).unlink()
        #     raise ValueError(
        #         "El archivo no es un formato admitido, solo se acepta archivos jpeg")

        return filename
