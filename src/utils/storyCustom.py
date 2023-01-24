import tempfile
from pathlib import Path
from typing import List
from urllib.parse import urlparse

from instagrapi.types import StoryBuild, StoryMention, StorySticker, StoryStickerLink

try:
    from moviepy.editor import CompositeVideoClip, ImageClip, TextClip, VideoFileClip
except ImportError:
    raise Exception("Please install moviepy==1.0.3 and retry")

try:
    from PIL import Image
except ImportError:
    raise Exception(
        "You don't have PIL installed. Please install PIL or Pillow>=8.1.1")


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

    def build_main(self, clip, max_duration: int = 0, link: str = "", title: str = '', price: str = '', shortcut_link: str = '') -> StoryBuild:
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
                ClipTitle = self.makeTextClip(y=250, title=title)
                clips.append(ClipTitle)
            if price != '':
                ClipPrice = self.makeTextClip(y=1000, title=price)
                clips.append(ClipPrice)
            if link != '':
                ClipLink = self.makeTextClip(
                    y=1100,
                    title=link,
                    shortcut_link=shortcut_link
                )
                link_sticker = StorySticker(
                    x=0.5,
                    y=0.9,
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
            .set_fps(60)\
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

    def makeTextClip(self, title: str = '', shortcut_link: str = '', y: int = 0):
        titleFinal = shortcut_link if shortcut_link != '' else title
        color = ''.join(self.color)
        font = ''.join(self.font)
        LinkClip = TextClip(
            " "+titleFinal+" ",
            color=color,
            bg_color="white",
            font=font,
            kerning=-1,
            fontsize=self.fontsize,
            stroke_width=1.5,
            method="label",
            align="center"
        )
        LinkClip = (
            LinkClip
            .set_position(("center", y))
        )
        return LinkClip

    def makeClipMedia(self, max_duration: int = 15, link: str = '', title: str = '', price: str = '', shortcut_link: str = ''):
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
                    shortcut_link=shortcut_link
                )
        else:
            clip = VideoFileClip(str(self.path), has_mask=True)
            build = self.build_main(
                clip=clip,
                max_duration=max_duration,
                link=link,
                title=title,
                price=price,
                shortcut_link=shortcut_link
            )
            clip.close()
            return build
