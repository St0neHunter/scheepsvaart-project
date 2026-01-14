import datetime
import os
import random
import time
from random import randint

import pgzrun
from pgzero.actor import Actor
from pgzhelper import *

win = False
caught = False

WIDTH = 600
HEIGHT = 600

background = Actor('background')
background.x = WIDTH / 2
background.y = HEIGHT / 2
background.scale = 18.75

background1 = Actor('background')
background1.x = WIDTH / 2
background1.y = HEIGHT / 2 - HEIGHT
background1.scale = 18.75

gerrit = Actor('standing')
gerrit.x = 400
gerrit.y = 550
gerrit.scale = 5
walkstage = 0
walkinglane = 0

lastupdate = float(time.time())


score = 0
goal = 50

# def on_mouse_move(pos, rel, buttons):
#
# def on_mouse_down(pos, button):
#
holdingLeft = False
holdingRight = False

def update():
    global gerrit, walkstage, lastupdate, score, walkinglane, holdingLeft, holdingRight

    ### start of keyboard crap ###
    if keyboard.left:
        if not holdingLeft:
            holdingLeft = True
            holdingRight = False
            if walkinglane == 0:
                score -= 5
            else:
                walkinglane -= 1
    elif holdingLeft: # keyboard.left == false
        holdingLeft = False

    if keyboard.right:
        if not holdingRight:
            holdingRight = True
            holdingLeft = False
            if walkinglane == 2:
                score -= 5
            else:
                walkinglane += 1
    elif holdingRight: # keyboard.right == false
        holdingRight = False
    ### end of keyboard crap ###

    if not lastupdate > float(time.time()) - 0.05:
        background.y += 5
        background1.y += 5
        # if background.y == HEIGHT:
        #     background.y = HEIGHT / 2 - HEIGHT
        if not walkstage == 8:
            gerrit.image = 'walk' + walkstage.__str__()
            gerrit.scale = 5
            walkstage += 1
        else:
            gerrit.image = 'walk0'
            gerrit.scale = 5
            walkstage = 1

        if walkinglane == 0:
            gerrit.x = 170
        elif walkinglane == 1:
            gerrit.x = 300
        elif walkinglane == 2:
            gerrit.x = 430

        lastupdate = time.time()


def draw():
    global score, goal, caught, win
    background.draw()
    background1.draw()

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