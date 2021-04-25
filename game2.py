import os
from random import randint as rd
import numpy as np
import pyglet as pg

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


class Arrow_object(pg.sprite.Sprite):
    def __init__(self, img, arr, vid, rand):
        super().__init__(img, arr[0][0], arr[0][1])
        self.vid = vid
        self.arr = arr
        self.count = 0
        self.len = len(arr)


class Arrow_class:
    col = 0
    arr = np.array([])

    def Arrow(self, n):
        for i in range(n):
            vid = rd(0, 2)
            rand = rd(0, 3)
            if vid == 0 or vid == 1:
                self.arr = np.append(self.arr, Arrow_object(arrow_vid[vid], arr_arrow[rand], vid, rand))
                self.arr[len(self.arr) - 1].rotation = 90 * rand
            else:
                pass

    def __init__(self):
        self.Arrow(1)
        f = open('High_games_count', 'r')
        self.high_games_col = int(f.read())
        f.close()

    def count(self, number):
        self.col += 1
        self.arr = np.delete(self.arr, number)
        if self.col > self.high_games_col:
            self.high_games_col = self.col

    def dead(self):

        global times_new_arrow, times_arrow

        times_new_arrow = 5
        times_arrow = 0

        if self.high_games_col == self.col:
            f = open('High_games_count','w')
            f.write(str(self.high_games_col))
            f.close()

        self.col = 0
        self.arr = np.array([])
        self.Arrow(1)


def display_get():
    display = window.get_display()
    screen = display.get_default_screen()
    return screen

window = pg.window.Window(680, 680)

center = pg.sprite.Sprite(img['center'], window.width / 2, window.height / 2)
ctrelka = pg.sprite.Sprite(img['ctrelka'], window.width / 2, window.height / 2, 0)

tick = 0.01
time_approach = 1
len_arr_arrow = int(time_approach / tick)

'''
Название массивов движения стрелок создавалось относительно места вылета стрелок 
arr_arrow - последовательность эл является определяющей в момент определения угла поворота стрелки
'''
arr_arrow1_left = np.concatenate((
    np.linspace(0, int((window.width - center.width) / 2 * 10) / 10, len_arr_arrow).reshape(len_arr_arrow, 1),
    np.array([window.height / 2] * len_arr_arrow).reshape(len_arr_arrow, 1)),
    axis=1
)
arr_arrow1_right = np.concatenate((
    np.linspace(window.width, int((window.width + center.width) / 2 * 10) / 10, len_arr_arrow).reshape(len_arr_arrow,
                                                                                                       1),
    np.array([window.height / 2] * len_arr_arrow).reshape(len_arr_arrow, 1)),
    axis=1
)
arr_arrow1_down = np.concatenate((
    np.array([window.width / 2] * len_arr_arrow).reshape(len_arr_arrow, 1),
    np.linspace(0, int((window.height - center.height) / 2 * 10) / 10, len_arr_arrow).reshape(len_arr_arrow, 1)),
    axis=1
)
arr_arrow1_up = np.concatenate((
    np.array([window.width / 2] * len_arr_arrow).reshape(len_arr_arrow, 1),
    np.linspace(window.height, int((window.height + center.height) / 2 * 10) / 10, len_arr_arrow).reshape(len_arr_arrow,
                                                                                                          1)),
    axis=1
)

arr_arrow = np.array([arr_arrow1_right, arr_arrow1_down, arr_arrow1_left, arr_arrow1_up])

games = Arrow_class()

# event_logger = pg.window.event.WindowEventLogger()  # Показывает все зарегестрированые события
# window.push_handlers(event_logger)


def arrow_hit_and_move():
    for i in range(len(games.arr)):
        if games.arr[i].count == games.arr[i].len - 1:

            # blue and yellow
            blue_head = games.arr[i].rotation == ctrelka.rotation and (games.arr[i].vid == 1 or games.arr[i].vid == 2)
            red_head = games.arr[i].rotation != ctrelka.rotation and games.arr[i].vid == 0

            if blue_head or red_head:
                games.count(i)
            else:
                games.dead()
            break

    for i in range(len(games.arr)):
        games.arr[i].count += 1  # arrow_move
        x, y = games.arr[i].arr[games.arr[i].count]
        games.arr[i].x = x
        games.arr[i].y = y


times_new_arrow = 5
times_arrow = 0


def new_arrow(dt):
    global times_arrow, times_new_arrow

    if int(times_arrow * 10) == times_new_arrow:
        games.Arrow(1)
        times_arrow = 0
        times_new_arrow = rd(1, 6)
    else:
        times_arrow += dt


def time1(dt):
    new_arrow(dt)
    arrow_hit_and_move()


pg.clock.schedule_interval(time1, tick)


@window.event
def on_draw():
    window.clear()
    center.draw()
    ctrelka.draw()
    for i in range(len(games.arr)):
        games.arr[i].draw()
    pg.text.Label(str(games.col), font_name='Calibri', font_size=15, color=[4, 217, 255, 255],
                  y=window.height - 15).draw()
    pg.text.Label('High '+ str(games.high_games_col), font_name='Calibri', font_size=15, color=[4, 217, 255, 255],
                  y=window.height - 30).draw()


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
