import extcolors
from colormap import rgb2hex
from PIL import Image, ImageDraw
import string
import random
from pathlib import Path
import ast


class ImageColor:
    @classmethod
    def getColorBackgroundImage(self, img_url):
        colors_x = extcolors.extract_from_path(img_url, tolerance=12, limit=12)
        colors_pre_list = str(colors_x).replace('([(', '').split(', (')[0:-1]
        df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
        # df_percent = [i.split('), ')[1].replace(')', '')
        #               for i in colors_pre_list]
        # convert RGB to HEX code
        # df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(", "")),
        #                        int(i.split(", ")[1]),
        #                        int(i.split(", ")[2].replace(")", ""))) for i in df_rgb]
        lista = [df_rgb[0], df_rgb[1]]
        return lista

    @classmethod
    def makeImageBackground(self, colorRGB):
        letters = string.ascii_lowercase
        randomString = ''.join(random.choice(letters) for i in range(10))
        fileName = f"{randomString}.jpg"
        dirPath = Path(__file__).parent.parent
        filePath = f"{dirPath}/uploads/{fileName}"

        imagen_degradada = self.makegradient(colorRGB)
        imagen_degradada.save(filePath, "PNG")
        return filePath

    @classmethod
    def makegradient(self, listaColores):
        width = 720
        height = 1280
        color1 = ast.literal_eval(listaColores[0])
        color2 = ast.literal_eval(listaColores[1])
        image = Image.new(mode="RGB", size=(width, height))
        draw = ImageDraw.Draw(image)

        for y in range(height):
            r, g, b = (
                color1[0] * (height - y) / height + color2[0] * y / height,
                color1[1] * (height - y) / height + color2[1] * y / height,
                color1[2] * (height - y) / height + color2[2] * y / height,
            )
            draw.line([(0, y), (width, y)], fill=(int(r), int(g), int(b)))

        return image
