import pyglet as pg
import os
from random import randint as rd
import time

pg.resource.path = ['./resources']
pg.resource.reindex()

img_list = list(os.walk('./resources'))[0][2]
print(img_list)
for i in img_list:
    if i[-3:] == 'psd':
        img_list.pop(img_list.index(i))

img = {i[:-4]: pg.resource.image(i) for i in img_list}
img['center'].anchor_x = img['center'].width / 2
img['center'].anchor_y = img['center'].height / 2
img['ctrelka'].anchor_x = img['ctrelka'].width / 2 - 10
img['ctrelka'].anchor_y = img['ctrelka'].height / 2
img['arrow'].anchor_y = img['arrow'].height / 2
arrow_vid = [img['arrow_red'], img['arrow_blue'], img['arrow_yellow']]
for i in range(len(arrow_vid)):
    arrow_vid[i].anchor_y = img['arrow_blue'].height / 2


class CenterObject(pg.sprite.Sprite):
    def __init__(self, img, x, y, vid):
        super().__init__(img, x, y)
        self.vid = vid


class Game:
    col = 0
    arr = []

    def Arrow(self, n):
        for i in range(n):
            vid = rd(0, 2)
            rand = rd(0, 3)

            if rand == 2:
                self.arr += [CenterObject(arrow_vid[vid], 0, window.height / 2, vid)]
            elif rand == 3:
                self.arr += [CenterObject(arrow_vid[vid], window.width / 2, window.height, vid)]
            elif rand == 0:
                self.arr += [CenterObject(arrow_vid[vid], window.width, window.height / 2, vid)]
            elif rand == 1:
                self.arr += [CenterObject(arrow_vid[vid], window.width / 2, 0, vid)]
            self.arr[len(self.arr) - 1].rotation = 90 * rand

    def __init__(self):
        self.Arrow(1)

    def count(self):
        self.col += 1
        self.arr = self.arr[1:]

    def dead(self):
        self.col = 0
        self.arr = []
        self.Arrow(1)

window = pg.window.Window(1000,1000)

games = Game()
center = CenterObject(img['center'], window.width / 2, window.height / 2, 0)
ctrelka = CenterObject(img['ctrelka'], window.width / 2, window.height / 2, 0)
times_arrow = 0
times_new_arrow = rd(2, 7)



event_logger = pg.window.event.WindowEventLogger()  # Показывает все зарегестрированые события
window.push_handlers(event_logger)

def arrow_hit():
    giper_p = 6.5

    if games.arr[0].x - giper_p == center.x - center.width / 2 or \
            games.arr[0].x + giper_p == center.x + center.width / 2 or \
            games.arr[0].y - giper_p == center.y - center.height / 2 or \
            games.arr[0].y + giper_p == center.y + center.height / 2:
        if (ctrelka.rotation == games.arr[0].rotation and (games.arr[0].vid == 1 or games.arr[0].vid == 2)) or \
                (ctrelka.rotation != games.arr[0].rotation and games.arr[0].vid == 0):
            games.count()
        else:
            games.dead()


def arrow_yellow_move(i):
    rad = 150
    speed = 0.5
    speed_okr = speed * (center.width / 2 + 3 * rad) / (rad - center.width / 2)



def arrow_move():
    speed = 5

    for i in range(len(games.arr)):
        #if games.arr[i].vid != 2:
            if games.arr[i].rotation == 180:
                games.arr[i].x += speed
            elif games.arr[i].rotation == 270:
                games.arr[i].y -= speed
            elif games.arr[i].rotation == 0:
                games.arr[i].x -= speed
            elif games.arr[i].rotation == 90:
                games.arr[i].y += speed
        #else:
            #arrow_yellow_move(i)


def new_arrow(dt):
    global times_arrow, times_new_arrow

    if int(times_arrow * 10) == times_new_arrow:
        games.Arrow(1)
        times_arrow = 0
        times_new_arrow = rd(2, 7)
    else:
        times_arrow += dt


def time1(dt):
    global times_arrow, times_new_arrow

    arrow_hit()
    arrow_move()
    new_arrow(dt)


pg.clock.schedule_interval(time1, 0.01)


@window.event
def on_draw():
    window.clear()
    center.draw()
    ctrelka.draw()
    for i in range(len(games.arr)):
        games.arr[i].draw()
    pg.text.Label(str(games.col), font_name='Calibri', font_size=15, color=[4, 217, 255, 255],
                  y=window.height - 15).draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pg.window.key.UP:
        ctrelka.rotation = 270
    elif symbol == pg.window.key.RIGHT:
        ctrelka.rotation = 0
    elif symbol == pg.window.key.DOWN:
        ctrelka.rotation = 90
    elif symbol == pg.window.key.LEFT:
        ctrelka.rotation = 180


pg.app.run()
