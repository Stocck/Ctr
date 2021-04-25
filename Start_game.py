import pyglet as pg
import os

pg.resource.path = ['./Start_game_img']
pg.resource.reindex()

img_list = list(os.walk('./Start_game_img'))[0][2]
print(img_list)
for i in img_list:
    if i[-3:] == 'psd':
        img_list.pop(img_list.index(i))

class Button:
    def __init__(self,text):
        pass