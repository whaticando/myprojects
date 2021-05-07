import random
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from utils import constant as C


class Valid_code():
    def __init__(self):
        self.temp = []
        self.width = C.valid_code_width
        self.height = C.valid_code_height

    def get_random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def get_random_code(self, request):
        from io import BytesIO
        from PIL import ImageDraw, Image, ImageFont
        f = BytesIO()

        image = Image.new(mode="RGB", size=(self.width, self.height), color=self.get_random_color())
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("simkai.ttf", size=32)

        for i in range(5):  # 这里的数字的范围，大写字母的范围，小写字母的范围，
            random_char = random.choice(
                [str(random.randint(0, 9)), chr(random.randint(65, 90)), chr(random.randint(97, 122))])

            draw.text((i * 20, 30), random_char, self.get_random_color(), font=font)
            self.temp.append(random_char)

        # 这里是干扰项

        '''点干扰'''
        for i in range(80):
            draw.point((random.randint(0, self.width), random.randint(0, self.height)), fill=self.get_random_color())

        '''线干扰'''
        # for i in range(10):
        #     x1 = random.randint(0, self.width)
        #     x2 = random.randint(0, self.width)
        #     y1 = random.randint(0, self.height)
        #     y2 = random.randint(0, self.height)
        #     draw.line((x1, x2, y1, y2), fill=self.get_random_color())

        '''圆弧干扰'''
        for i in range(40):
            draw.point([random.randint(0, self.width), random.randint(0, self.height)])
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            draw.arc((x, y, x + 4, y + 4), 0, 90, fill=self.get_random_color())

        image.save(f, "png")
        data = f.getvalue()
        request.session["random_code_str"] = "".join(self.temp)

        return HttpResponse(data)

    #     # 法1“
    #     # f = open('1.jpg',"rb")
    #     # data = f.read()
    #
    #     # 法2
    #     # image = Image.new(mode="RGB", size=(120, 80), color=get_random())
    #     # f = open("code.png", "wb")
    #     # image.save(f, "png")
    #     # f = open("code.png", "rb")
    #     # data = f.read()
    #     # return HttpResponse(data)
    #
    #     # 法3
    #     # from io import BytesIO
    #     # image = Image.new(mode="RGB", size=(120, 80), color=get_random())
    #     # f = BytesIO()
    #     # image.save(f,"png")
    #     # data = f.getvalue()
    #     # return HttpResponse(data)
    #
    #     # 法4
