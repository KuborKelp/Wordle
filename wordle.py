'''
    Author:KuborKelp
    Name:Wordle
'''
import os
from PIL import Image, ImageFont, ImageDraw

ttf_path = "./HarmonyOS_Sans_SC_Medium.ttf"
cache_path = "./cache/wordle/"


class Wordle:
    def __init__(self, keyword: str, length: int, maxround: int, if_draw: bool):
        self.MAXROUND = maxround
        self.keyword = keyword.upper()
        self.length = length
        self.round = 0
        self.word_history = [""] * self.MAXROUND  # record the words that players has guessed
        self.status_history = [["N"] * self.length] * self.MAXROUND  # record the words that players has guessed with
        # the symbol in "T F G N"
        # drawing
        self.if_draw = if_draw
        self.img = None
        self.game_status = True
        self.path = cache_path

        if not (len(keyword) == length and keyword.isalpha()):
            print("Unable to set the word!")

        # initial image
        if if_draw:
            self.ttf = ImageFont.truetype(ttf_path, 25, encoding='utf-8')

            self.img = Image.new('RGB', (length * 50 + 20, maxround * 50 + 20), color='White')
            self.pix = self.img.load()
            for i in range(length):  # 列
                for j in range(maxround):  # 行
                    x1 = 10 + i * 50 + 5
                    y1 = 10 + j * 50 + 5
                    x2 = x1 + 40
                    y2 = y1 + 40
                    for x in range(x1, x2 + 1):
                        self.pix[x, y1] = (128, 128, 128)
                        self.pix[x, y2] = (128, 128, 128)
                    for y in range(y1, y2):
                        self.pix[x1, y] = (128, 128, 128)
                        self.pix[x2, y] = (128, 128, 128)

    def next(self, word):
        word = word.upper()
        ret = None
        if len(word) != self.length:
            ret = f"Check the length of the word.It should be {self.length}"
        elif word in self.word_history:
            ret = f"you have guessed the word:{word}"
        else:
            self.word_history[self.round] = word
            lst = []
            for i in range(0, self.length):
                if word[i] == self.keyword[i]:
                    lst.append("T")
                elif word[i] in self.keyword and word.count(self.keyword[i]) <= self.keyword.count(self.keyword[i]):
                    lst.append("G")
                else:
                    lst.append("F")
            self.status_history[self.round] = lst
            if word == self.keyword:
                self.game_status = False
                ret = "Win!"
            print(self.word_history)
            print(self.status_history)
            if self.if_draw:
                self.draw(word, lst)
                self.img.save(f"{self.path}{self.round}.png")
            self.round += 1
        return ret

    def draw(self, word, lst):
        for i in range(self.length):
            y = self.round
            x = i
            if lst[i] == "T":
                self.green(x, y)
            elif lst[i] == "F":
                self.grey(x, y)
            else:
                self.yellow(x, y)
            self.write(word[i], x, y)
        pass

    def write(self, letter, x, y):
        x = 11 + x * 50 + 12
        y = 11 + y * 50 + 10
        img_draw = ImageDraw.Draw(self.img)
        img_draw.text((x, y), letter, fill=(255, 255, 255), font=self.ttf, align='right')

    def green(self, x, y):
        color = Image.new('RGB', (39, 39), color='Green')
        self.img.paste(color, (11 + x * 50 + 5, 11 + y * 50 + 5))

    def yellow(self, x, y):
        color = Image.new('RGB', (39, 39), color=(209, 198, 103))
        self.img.paste(color, (11 + x * 50 + 5, 11 + y * 50 + 5))

    def grey(self, x, y):
        color = Image.new('RGB', (39, 39), color=(128, 128, 128))
        self.img.paste(color, (11 + x * 50 + 5, 11 + y * 50 + 5))


if __name__ == "__main__":
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)
    print("Hello,Wordle!")
    game = None
    while True:
        if not game:
            x = input("enter 0 to exit \nenter 1 to start a game\n")
            if x == "0":
                game = None
                print("The game has been killed")
            else:
                game = Wordle(keyword="oonpgwcnmd", length=10, maxround=10, if_draw=True)
        else:
            if game.round >= game.MAXROUND:
                game = None
                print("Boy,what can I say!")
            else:
                word = input("Guess:")
                print(game.next(word=word))
                if not game.game_status:  # you won
                    game = None
