import random
import time

import pgzero.game
import pgzrun
from pgzhelper import *

startMenu = True
tutorial = False
win = False
lose = False
lastUpdate = float(time.time())

WIDTH = 600
HEIGHT = 600
TITLE = "Gerrit"

startButton = Actor('startbutton')
startButton.x = WIDTH / 2 + 210
startButton.y = HEIGHT / 2 + 30
startButton.scale = 5

tutorialButton = Actor('tutorialbutton')
tutorialButton.x = WIDTH / 2 + 210
tutorialButton.y = HEIGHT / 2 + 95
tutorialButton.scale = 2.5

quitButton = Actor('quitbutton')
quitButton.x = WIDTH / 2 + 210
quitButton.y = HEIGHT / 2 + 160
quitButton.scale = 5

background = Actor('background')
background.x = WIDTH / 2
background.y = HEIGHT / 2
background.scale = 18.75

background1 = Actor('background')
background1.x = WIDTH / 2
background1.y = HEIGHT / 2 - HEIGHT
background1.scale = 18.75

homescreenbackground = Actor('homescreen0')
homescreenbackground.x = WIDTH / 2
homescreenbackground.y = HEIGHT / 2
homescreenbackground.scale = 12
homescreenanimation = 0

gerrit = Actor('standing')
gerrit.x = 400
gerrit.y = 550
gerrit.scale = 5
walkStage = 0
walkingLane = 0
hurtTime = 0

score = 0
warningsleft = 1
goal = 50

walkingLane1pos = 170
walkingLane2pos = 300
walkingLane3pos = 430

dummyprop = Actor("chicken")
dummyprop.x = -100
props = [dummyprop]

random.seed(time.time())

def on_mouse_down(pos, button):
    global startMenu, startButton, tutorialButton, tutorial
    if startButton.collidepoint(pos) and startMenu:
        startMenu = False
    elif tutorialButton.collidepoint(pos):
        tutorial = not tutorial
    elif quitButton.collidepoint(pos):
        pgzero.game.exit()

holdingLeft = False
holdingRight = False

def update():
    global gerrit, walkStage, lastUpdate, score, goal, walkingLane, holdingLeft, holdingRight, hurtTime, homescreenanimation, win, lose, warningsleft

    if startMenu:
        if not lastUpdate > float(time.time()) - 0.15:
            homescreenbackground.image = 'homescreen' + homescreenanimation.__str__()
            homescreenbackground.scale = 12
            if homescreenanimation == 19:
                homescreenanimation = 0
            homescreenanimation += 1
            lastUpdate = time.time()
        return
    if lose or win:
        return

    if score >= goal:
        win = True
        return
    elif score <= -10:
        lose = True
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
        prop.y += 5
        if prop.y > HEIGHT + prop.height:
            props.remove(prop)
            continue
        if prop.colliderect(gerrit):
            if prop.image == 'chicken':
                score += 5
            elif prop.image == 'porridge':
                score += 2
            elif prop.image == 'scheepsbeschuit':
                score += 1
            elif prop.image == "crate":
                lose = True
                continue
            props.remove(prop)
        elif prop.y > HEIGHT  + prop.height:
            props.remove(prop)

        for prop1 in props:
            # if prop1.image == "crate" or prop.image == "crate":
            #     continue
            if prop1 == prop:
                continue
            if prop.colliderect(prop1):
                props.remove(prop)
            #elif int(prop.y) in range(int(prop1.y) + int(prop1.height), int(prop1.y) - int(prop1.height)):
            #    props.remove(prop)

    background.y += 5
    background1.y += 5
    if background.y == HEIGHT + HEIGHT / 2:
        background.y = HEIGHT / 2 - HEIGHT
    if background1.y == HEIGHT + HEIGHT / 2:
        background1.y = HEIGHT / 2 - HEIGHT


    if not lastUpdate > float(time.time()) - 0.05: # main game loop runs less frequent
        if random.randint(0, 200) == 1:
            newprop = Actor("chicken")
            newprop.y = -200
            newprop.x = random.choice([walkingLane1pos, walkingLane2pos, walkingLane3pos])
            newprop.scale = 5
            props.append(newprop)
        elif random.randint(0, 125) == 1:
            newprop = Actor("porridge")
            newprop.y = -200
            newprop.x = random.choice([walkingLane1pos, walkingLane2pos, walkingLane3pos])
            newprop.scale = 5
            props.append(newprop)
        elif random.randint(0, 75) == 1:
            newprop = Actor("scheepsbeschuit")
            newprop.y = -200
            newprop.x = random.choice([walkingLane1pos, walkingLane2pos, walkingLane3pos])
            newprop.scale = 5
            props.append(newprop)
        elif random.randint(0, 50) == 1:
            newprop = Actor("crate")
            newprop.y = -100
            newprop.x = random.choice([walkingLane1pos, walkingLane2pos, walkingLane3pos])
            newprop.scale = 6.5
            props.append(newprop)
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
    global score, goal, lose, win

    background.draw()
    background1.draw()
    for prop in props:
        prop.draw()

    if tutorial:
        screen.fill((103, 190, 217))
        screen.draw.text(
            'In this game you play as Gerrit, a crewmate.\n'
            'To survive he needs to eat, but that\'s not easy...\n'
            '\n'
            'There is three types of food Gerrit can find and eat:\n'
            'ship\'s biscuit: 1 point\n'
            'porridge: 2 point\'s\n'
            'chicken: 5 points BUT this food is not ment for crewmates.\n'
            'There is a 50% change of Gerrit being caught and losing a\n'
            'warning and the second time being thrown off the ship.\n',
            (20, 120),
            color=(0, 0, 0),
            fontsize=30
        )
        tutorialButton.draw()

        screen.draw.text(
            'Controls\n'
            ' - Move left     <\n'
            ' - Move right   >\n'
            ' - Jump           ^',
            (10, 10),
            color=(0, 0, 0),
            fontsize=30
        )
        return
    elif startMenu:
        screen.fill((103, 190, 217))
        homescreenbackground.draw()
        screen.draw.text(
            'Ship Runner',
            (210, 190),
            color=(0, 0, 0),
            fontsize=60
        )
        startButton.draw()
        tutorialButton.draw()
        quitButton.draw()

    elif win:
        screen.draw.text(
            'You won!',
            center=(WIDTH / 2, HEIGHT / 2),
            color=(255, 255, 255),
            fontsize=60
        )
        screen.draw.text(
            'Score: ' + str(score) + '/' + goal.__str__(),
            (15, 10), color=(255, 255, 255),
            fontsize=30
        )
    elif lose:
        screen.draw.text(
            'You lost!',
            center=(WIDTH / 2, HEIGHT / 2),
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
        screen.draw.text(
            'Warnings left: ' + str(warningsleft),
            (15, 30), color=(255, 255, 255),
            fontsize=30
        )


pgzrun.go() # Moet de laatste regel zijn