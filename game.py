import os
import random
from random import randint

import pgzrun
from pgzero.actor import Actor

win = False
caught = False

WIDTH = 600
HEIGHT = 600

gerrit = Actor('gemred')
gerrit.x = 400
gerrit.y = 550
score = 0
goal = 50

# def on_mouse_move(pos, rel, buttons):
#
# def on_mouse_down(pos, button):
#



def update():
    if keyboard.left:
        gerrit.x = gerrit.x - 5
    if keyboard.right:
        gerrit.x = gerrit.x + 5


def draw():
    global score, goal, caught, win
    screen.fill((0, 0, 0))

    if win:
        screen.draw.text(
            'Gewonnen!',
            (450, 200),
            color=(255, 255, 255),
            fontsize=60
        )
    else:
        gerrit.draw()
        screen.draw.text(
            'Score: ' + str(score) + '/' + goal.__str__(),
            (15, 10), color=(255, 255, 255),
            fontsize=30
        )


pgzrun.go() # Moet de laatste regel zijn