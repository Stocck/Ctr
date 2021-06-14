import os
from random import randint as rd
import numpy as np
import pyglet as pg

pg.resource.path = ['./cnopki']
pg.resource.reindex()

img = pg.resource.image('point.png')
img.anchor_x, img.anchor_y = 2, 2
point = pg.sprite.Sprite(img, x=450, y=450)
window = pg.window.Window(900, 900)

DeltaTime = 2  # 2sec = T_Spawn_arrow - T_Dead_arrow
fps = 60
rad = 400
center = {'x': 450,
          'y': 450}
x0, y0 = center['x'], center['y']
arr_move = []

for i in np.linspace(np.pi, np.pi / 2, DeltaTime * fps // 2):
    arr_move.append(np.array([rad * np.cos(i) + x0, rad * np.sin(i) + y0]))
arr_move = np.array(arr_move)
print(arr_move)


@window.event
def on_draw():
    for i in arr_move:
        point.x, point.y = i
        point.draw()


pg.app.run()
