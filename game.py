import random
import time
import pgzrun
from pgzhelper import *
import secrets
import numpy.random as rnd

startMenu = True
win = False
caught = False
lastUpdate = float(time.time())

WIDTH = 600
HEIGHT = 600

startButton = Actor('gemred')
startButton.x = WIDTH / 2
startButton.y = HEIGHT / 2
startButton.scale = 2

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
walkStage = 0
walkingLane = 0
hurtTime = 0

score = 0
goal = 50

walkingLane1pos = 170
walkingLane2pos = 300
walkingLane3pos = 430

dummyprop = Actor("chicken")
dummyprop.x = -100
props = [dummyprop]

random.seed(time.time())

def on_mouse_down(pos, button):
    global startMenu, startButton
    if startButton.collidepoint(pos) and startMenu:
        startMenu = False

holdingLeft = False
holdingRight = False

def update():
    global gerrit, walkStage, lastUpdate, score, walkingLane, holdingLeft, holdingRight, hurtTime

    if startMenu:
        return

    ### start of keyboard handling ###
    if keyboard.left:
        if not holdingLeft:
            holdingLeft = True
            holdingRight = False
            if walkingLane == 0:
                score -= 2
                gerrit.image = 'hurt'
                gerrit.scale = 5
                hurtTime = 1
            else:
                walkingLane -= 1
    elif holdingLeft: # keyboard.left == false
        holdingLeft = False

    if keyboard.right:
        if not holdingRight:
            holdingRight = True
            holdingLeft = False
            if walkingLane == 2:
                score -= 2
                gerrit.image = 'hurt'
                gerrit.scale = 5
                hurtTime = 1
            else:
                walkingLane += 1
    elif holdingRight: # keyboard.right == false
        holdingRight = False
    ### end of keyboard handling ###

    for prop in props:
        prop.y += 4
        if prop.colliderect(gerrit):
            score += 1
            props.remove(prop)
        elif prop.y > HEIGHT  + prop.height:
            props.remove(prop)

        for prop1 in props:
            if prop1 == prop:
                continue
            if prop.colliderect(prop1):
                props.remove(prop)
            #elif int(prop.y) in range(int(prop1.y) + int(prop1.height), int(prop1.y) - int(prop1.height)):
             #   props.remove(prop)

    background.y += 4
    background1.y += 4
    if background.y == HEIGHT + HEIGHT / 2:
        background.y = HEIGHT / 2 - HEIGHT
    if background1.y == HEIGHT + HEIGHT / 2:
        background1.y = HEIGHT / 2 - HEIGHT

    randomint = round(rnd.random() * 10)
    # print(randomint.__str__())
    if randomint == 10:
        newprop = Actor("chicken")
        newprop.y = -100
        newprop.x = random.choice([walkingLane1pos, walkingLane2pos, walkingLane3pos])
        newprop.scale = 5
        props.append(newprop)


    if not lastUpdate > float(time.time()) - 0.05: # update gerrit less frequent
        if hurtTime == 3:
            hurtTime = 0
        elif hurtTime > 0:
            hurtTime += 1
        else:
            if not walkStage == 8:
                gerrit.image = 'walk' + walkStage.__str__()
                gerrit.scale = 5
                walkStage += 1
            else:
                gerrit.image = 'walk0'
                gerrit.scale = 5
                walkStage = 1

            if walkingLane == 0:
                gerrit.x = walkingLane1pos
            elif walkingLane == 1:
                gerrit.x = walkingLane2pos
            elif walkingLane == 2:
                gerrit.x = walkingLane3pos

        lastUpdate = time.time()


def draw():
    global score, goal, caught, win

    background.draw()
    background1.draw()
    for prop in props:
        prop.draw()

    if startMenu:
        screen.fill((103, 190, 217))
        screen.draw.text(
            'Welcome!',
            (210, 190),
            color=(255, 255, 255),
            fontsize=60
        )
        screen.draw.text(
            'In this game you play as Gerrit, a crewmate.\n'
            'To survive he needs to eat but that\'s not easy',
            (100, 230),
            color=(255, 255, 255),
            fontsize=30
        )
        startButton.draw()

        screen.draw.text(
            'Controls\n'
            ' - Move left     <\n'
            ' - Move right   >\n'
            ' - Jump           ^',
            (10, 10),
            color=(255, 255, 255),
            fontsize=30
        )

    elif win:
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