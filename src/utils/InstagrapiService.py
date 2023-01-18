from instagrapi import Client
from instagrapi.types import StoryLink
from instagrapi.story import StoryBuilder
from pathlib import Path


class InstagrapiService():
    @classmethod
    def setParameters(self, request):
        file = request.files
        req = self.validateFields(request.form)
        type = request.path
        acceptedExt = 'mp4' if type.endswith('Video') else 'jpeg'
        pathFile = self.saveFiles(file['file'], acceptedExt)
        data = {
            'account': req['account'],
            'password': req['password'],
            'description': req.get('description') or '',
            'alias': req.get('alias') or '',
            'file': pathFile,
            'url': req.get('url') or []
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
        cl = self.isLogin(obj)
        mediapath = obj['file']
        cl.photo_upload(
            path=Path(mediapath),
            caption=obj['description'],
        )
        Path(mediapath).unlink()

    @classmethod
    def uploadVideo(self, obj):
        cl = self.isLogin(obj)
        mediapath = obj['file']
        cl.video_upload(
            path=Path(mediapath),
            caption=obj['description'],
        )
        Path(mediapath).unlink()

    @classmethod
    def uploadStoryVideo(self, obj):
        cl = self.isLogin(obj)
        mediapath = obj['file']
        buildout = StoryBuilder(
            mediapath,
            obj['alias'],
            None
        ).video(30)

        cl.video_upload_to_story(
            path=buildout.path,
            links=[] if obj['url'] == [] else [StoryLink(
                webUri=obj['url'],
                # x=0.1,
                # y=0.2,
                # width=5,
                # height=5
            )],
        )
        Path(mediapath).unlink()

    @classmethod
    def uploadStoryPhoto(self, obj):
        cl = self.isLogin(obj)
        mediapath = obj['file']

        buildout = StoryBuilder(
            path=mediapath,
            caption=obj['alias'],
            bgpath=None
        ).vide(30)

        cl.photo_upload_to_story(
            path=buildout.path,
            links=[StoryLink(webUri=obj['url'])],
        )
        Path(mediapath).unlink()

    @classmethod
    def validateFields(self, obj):
        if obj['account'] == '' or obj['password'] == '':
            raise ValueError("Los campos account y password son obligatorios")
        return obj

    @classmethod
    def saveFiles(self, file, acceptedExt):
        if file.filename == '':
            raise ValueError("El campo file es obligatorio")
        path = Path(__file__).parent.parent
        filename = f"{path}/uploads/{file.filename}"
        file.save(filename)

        file_path = Path(filename)
        if file_path.suffix != f".{acceptedExt}":
            Path(filename).unlink()
            raise ValueError(
                "El archivo no es un formato admitido, solo se acepta archivos jpeg")
        return filename
