import extcolors
from colormap import rgb2hex
from PIL import Image
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
        return df_rgb[0]

    @classmethod
    def makeImageBackground(self, colorRGB):
        colorRGB = ast.literal_eval(colorRGB)
        w = 720
        h = 1280
        # start creating gradient
        pixel_list = []
        pixel_w = []
        # colour at 0,0
        start1 = (255, 255, 255)
        # start1 = (255, 213, 215)
        s = list(start1)
        pixel_list.append(start1)
        # print('Position zero:', pixel_list[0])

        # colour at end
        # end1 = (174, 15, 15)
        end1 = colorRGB
        e = list(end1)

        # in case you want to change the final colour you could use f to adjust otherwise just keep it at 1
        f = 1

        # transition per line
        r = (s[0] - e[0])/w*f
        g = (s[1] - e[1])/w*f
        b = (s[2] - e[2])/w*f

        t = ()

        for j in range(0, w):
            t = pixel_list[j]

            # convert pixel tuple to a list and recalculate
            li = list(t)
            li[0] = int(max((li[0] - r*j), 0))
            li[1] = int(max((li[1] - g*j), 0))
            li[2] = int(max((li[2] - b*j), 0))
            z = (li[0], li[1], li[2])
            final_t = tuple(z)
            # print('final_t:', final_t) if you want to show the list of pixel values
            pixel_list[j] = final_t
            for i in range(0, h):
                pixel_w = []
                pixel_w.append(final_t)
                pixel_list.extend(pixel_w)

        l = len(pixel_list)

        del pixel_list[l-1:]

        letters = string.ascii_lowercase
        randomString = ''.join(random.choice(letters) for i in range(10))
        fileName = f"{randomString}.jpg"
        dirPath = Path(__file__).parent.parent
        filePath = f"{dirPath}/uploads/{fileName}"
        im = Image.new('RGB', (w, h))
        im.putdata(pixel_list)
        im.save(filePath)
        return filePath
