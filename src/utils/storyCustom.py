import tempfile
from pathlib import Path
from typing import List
from urllib.parse import urlparse
from instagrapi.types import StoryBuild, StoryMention, StorySticker, StoryStickerLink
from moviepy.editor import CompositeVideoClip, ImageClip, TextClip, VideoFileClip
from PIL import Image, ImageOps, ImageDraw, ImageFont
import cv2
import numpy as np
import string
import random
import imageio
import ast


class StoryBuilder:
    """
    Helpers for Story building
    """

    width = 720
    height = 1280
    # width = 1080
    # height = 1920

    def __init__(
        self,
        path: Path,
        caption: str = "",
        mentions: List[StoryMention] = [],
        bgpath: Path = None,
        color: str = "",
        font: str = "",
        fontsize: int = 0,
    ):
        """
        Initialization function

        Parameters
        ----------
        path: Path
            Path for a file
        caption: str, optional
            Media caption, default value is ""
        mentions: List[StoryMention], optional
            List of mentions to be tagged on this upload, default is empty list
        bgpath: Path
            Path for a background image, default value is ""
        color: str, optional
        font: str, optional
        fontsize: int, optional
        Returns
        -------
        Void
        """
        self.path = Path(path)
        self.caption = caption
        self.mentions = mentions
        self.bgpath = Path(bgpath) if bgpath else None
        self.color = color,
        self.font = font,
        self.fontsize = fontsize

    def build_main(self, clip, max_duration: int = 0, link: str = "", title: str = '', price: str = '', shortcut_link: str = '', colors: any = []) -> StoryBuild:
        """
        Build clip

        Parameters
        ----------
        clip: (VideoFileClip, ImageClip)
            An object of either VideoFileClip or ImageClip
        max_duration: int, optional
            Duration of the clip if a video clip, default value is 0
        font: str, optional
            Name of font for text clip
        fontsize: int, optional
            Size of font
        color: str, optional
            Color of text

        Returns
        -------
        StoryBuild
            An object of StoryBuild
        """
        clips = []
        stickers = []
        # Background
        if self.bgpath:
            assert self.bgpath.exists(
            ), f"Wrong path to background {self.bgpath}"
            background = ImageClip(str(self.bgpath))
            clips.append(background)
        media_clip = clip.set_position(
            ("center", "center")
        )
        clips.append(media_clip)
        if link:
            if title != '':
                ClipTitle = self.makeTextClip(
                    y=110,
                    title=title,
                    colors=colors,
                    fontSize=64,
                    withIcon=False
                )
                clips.append(ClipTitle)
            if price != '':
                ClipPrice = self.makeTextClip(
                    y=240,
                    title=price,
                    fontSize=48,
                    withIcon=False
                )
                clips.append(ClipPrice)
            if link != '':
                ClipLink = self.makeTextClip(
                    y=1000,
                    title=link,
                    fontSize=48,
                    shortcut_link=shortcut_link,
                    withIcon=True
                )
                link_sticker = StorySticker(
                    x=0.5,
                    y=0.8,
                    width=round(
                        ClipLink.size[0] / self.width, 7
                    ),
                    height=round(
                        ClipLink.size[1] / self.height, 7
                    ),
                    rotation=0.0,
                    type="story_link",
                    extra=dict(
                        link_type="web",
                        url=str(link),
                        tap_state_str_id="link_sticker_default",
                    )
                )
                clips.append(ClipLink)
                stickers.append(link_sticker)
        duration = max_duration
        if getattr(clip, 'duration', None):
            if duration > int(clip.duration) or not duration:
                duration = int(clip.duration)
        destination = tempfile.mktemp(".mp4")
        cvc = CompositeVideoClip(clips, size=(self.width, self.height))\
            .set_fps(30)\
            .set_duration(duration)
        cvc.write_videofile(destination, codec="libx264",
                            audio=True, audio_codec="aac")
        paths = []
        if duration > 15:
            for i in range(duration // 15 + (1 if duration % 15 else 0)):
                path = tempfile.mktemp(".mp4")
                start = i * 15
                rest = duration - start
                end = start + (rest if rest < 15 else 15)
                sub = cvc.subclip(start, end)
                sub.write_videofile(path, codec="libx264",
                                    audio=True, audio_codec="aac")
                paths.append(path)
        return StoryBuild(mentions=[], path=destination, paths=[], stickers=stickers)

    def makeTextClip(self, title: str = '', shortcut_link: str = '', y: int = 0, colors: any = [], fontSize: int = 48, withIcon: bool = True):
        texto = shortcut_link if shortcut_link != '' else title
        tamano_fuente = fontSize
        color_fondo = (255, 255, 255, 1)
        color_texto = (0, 0, 0, 0)
        path = Path(__file__).parent.parent

        archivo_icono = f"{path}/icons/link_icon.ico"
        fuente = f"{path}/fonts/Roboto-Black.ttf"

        if(withIcon):
            etiqueta = self.crear_etiqueta_con_icono(
                texto,
                fuente,
                tamano_fuente,
                color_fondo,
                color_texto,
                archivo_icono
            )
        else:
            etiqueta = self.crear_etiqueta_sin_icono(
                texto,
                fuente,
                tamano_fuente,
                color_fondo,
                color_texto
            )
        randomName = self.generateRandomString()
        filenameLink = f"{path}/uploads/{randomName}.png"
        etiqueta.save(filenameLink, "PNG")

        LinkClip = ImageClip(filenameLink)
        LinkClip = (LinkClip.set_position(("center", y)))
        Path(filenameLink).unlink()

        return LinkClip

    def crear_etiqueta_con_icono(self, texto, fuente, tamano_fuente, color_fondo, color_texto, archivo_icono, padding=20):
        # Cargar la fuente y el icono
        font = ImageFont.truetype(fuente, tamano_fuente)
        icono = Image.open(archivo_icono).convert("RGBA")

        # Escalar el icono para que coincida con la altura del texto
        ancho_icono, alto_icono = icono.size
        factor_escala = tamano_fuente / alto_icono
        icono = icono.resize((int(ancho_icono * factor_escala),
                              int(alto_icono * factor_escala)), Image.ANTIALIAS)

        # Calcular el tamaño del texto y el tamaño de la etiqueta con el padding
        tamaño_texto = font.getsize(texto)
        tamaño_etiqueta = (tamaño_texto[0] + icono.width + 3 *
                           padding, max(tamaño_texto[1], icono.height) + 2 * padding)

        # Crear una imagen con el color de fondo especificado y agregar el texto
        imagen = Image.new("RGBA", tamaño_etiqueta, color_fondo)
        draw = ImageDraw.Draw(imagen)

        # Dibujar el icono y el texto en la imagen
        imagen.paste(
            icono, (padding, (tamaño_etiqueta[1] - icono.height) // 2), icono)
        draw.text((icono.width + 2 * padding, padding),
                  texto, font=font, fill=color_texto)

        # Redondear las esquinas de la etiqueta
        redondeado = 15
        mascara = Image.new("L", tamaño_etiqueta, 0)
        draw_mascara = ImageDraw.Draw(mascara)
        draw_mascara.rectangle(
            [redondeado, 0, tamaño_etiqueta[0] - redondeado, tamaño_etiqueta[1]], fill=255)
        draw_mascara.rectangle(
            [0, redondeado, tamaño_etiqueta[0], tamaño_etiqueta[1] - redondeado], fill=255)
        draw_mascara.ellipse([0, 0, 2 * redondeado, 2 * redondeado], fill=255)
        draw_mascara.ellipse([tamaño_etiqueta[0] - 2 * redondeado,
                              0, tamaño_etiqueta[0], 2 * redondeado], fill=255)
        draw_mascara.ellipse([0, tamaño_etiqueta[1] - 2 * redondeado,
                              2 * redondeado, tamaño_etiqueta[1]], fill=255)
        draw_mascara.ellipse([tamaño_etiqueta[0] - 2 * redondeado, tamaño_etiqueta[1] -
                              2 * redondeado, tamaño_etiqueta[0], tamaño_etiqueta[1]], fill=255)
        imagen.putalpha(mascara)
        return imagen

    def crear_etiqueta_sin_icono(self, texto, fuente, tamano_fuente, color_fondo, color_texto, padding=20):
        ancho_max = 600
        # Cargar la fuente
        font = ImageFont.truetype(fuente, tamano_fuente)

        # Dividir el texto en líneas según el ancho máximo
        lineas = self.dividir_texto(texto, font, ancho_max)
        altura_lineas = tamano_fuente * len(lineas)

        # Calcular el ancho máximo de las líneas
        ancho_max_linea = max(font.getsize(linea)[0] for linea in lineas)
        ancho_etiqueta = min(ancho_max, ancho_max_linea) + 2 * padding

        # Calcular el tamaño de la etiqueta con el padding
        altura_etiqueta = altura_lineas + 2 * padding

        # Crear una imagen con el color de fondo especificado y agregar el texto
        imagen = Image.new(
            "RGBA", (ancho_etiqueta, altura_etiqueta), color_fondo)
        draw = ImageDraw.Draw(imagen)

        # Dibujar el texto centrado en la imagen
        for i, linea in enumerate(lineas):
            ancho_linea = font.getsize(linea)[0]
            posicion_x = padding + (ancho_etiqueta - 2 *
                                    padding - ancho_linea) // 2
            draw.text((posicion_x, padding + i * tamano_fuente),
                      linea, font=font, fill=color_texto)

        # Redondear las esquinas de la etiqueta
        redondeado = 20
        mascara = Image.new("L", (ancho_etiqueta, altura_etiqueta), 0)
        draw_mascara = ImageDraw.Draw(mascara)
        draw_mascara.rectangle(
            [redondeado, 0, ancho_etiqueta - redondeado, altura_etiqueta], fill=255)
        draw_mascara.rectangle(
            [0, redondeado, ancho_etiqueta, altura_etiqueta - redondeado], fill=255)
        draw_mascara.ellipse([0, 0, 2 * redondeado, 2 * redondeado], fill=255)
        draw_mascara.ellipse([ancho_etiqueta - 2 * redondeado,
                              0, ancho_etiqueta, 2 * redondeado], fill=255)
        draw_mascara.ellipse([0, altura_etiqueta - 2 * redondeado,
                              2 * redondeado, altura_etiqueta], fill=255)
        draw_mascara.ellipse([ancho_etiqueta - 2 * redondeado, altura_etiqueta -
                              2 * redondeado, ancho_etiqueta, altura_etiqueta], fill=255)
        imagen.putalpha(mascara)

        return imagen

    def dividir_texto(self, texto, font, ancho_max):
        palabras = texto.split()
        lineas = []
        linea_actual = []

        for palabra in palabras:
            medida_linea = font.getsize(' '.join(linea_actual + [palabra]))[0]
            if medida_linea <= ancho_max:
                linea_actual.append(palabra)
            else:
                lineas.append(' '.join(linea_actual))
                linea_actual = [palabra]

        if linea_actual:
            lineas.append(' '.join(linea_actual))

        return lineas

    def generateRandomString(self):
        randomName = ''.join(random.choice(string.ascii_lowercase)
                             for i in range(10))
        return randomName

    def makeClipMedia(self, max_duration: int = 15, link: str = '', title: str = '', price: str = '', shortcut_link: str = '', colors: any = []):
        clip = ""
        typeFile = self.path.suffix
        if typeFile == '.jpeg':
            with Image.open(self.path) as im:
                image_width, image_height = im.size
                width_reduction_percent = (self.width / float(image_width))
                height_in_ratio = int(
                    (float(image_height) * float(width_reduction_percent)))
                clip = ImageClip(str(self.path)).resize(
                    width=self.width,
                    height=height_in_ratio
                )
                return self.build_main(
                    clip=clip,
                    max_duration=max_duration,
                    link=link,
                    title=title,
                    price=price,
                    shortcut_link=shortcut_link,
                    colors=colors,
                )
        else:
            clip = VideoFileClip(str(self.path), has_mask=True)
            build = self.build_main(
                clip=clip,
                max_duration=max_duration,
                link=link,
                title=title,
                price=price,
                shortcut_link=shortcut_link,
                colors=colors,
            )
            clip.close()
            return build
