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
TITLE = "Ship Runner"

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

backButton = Actor('backbutton')
backButton.x = WIDTH / 2 + 210
backButton.y = HEIGHT / 2 + 160
backButton.scale = 5

backGround = Actor('background')
backGround.x = WIDTH / 2
backGround.y = HEIGHT / 2
backGround.scale = 18.75

backGround1 = Actor('background')
backGround1.x = WIDTH / 2
backGround1.y = HEIGHT / 2 - HEIGHT
backGround1.scale = 18.75

homeScreenBackground = Actor('homescreen0')
homeScreenBackground.x = WIDTH / 2
homeScreenBackground.y = HEIGHT / 2
homeScreenBackground.scale = 12
homeScreenAnimation = 0

gerrit = Actor('standing')
gerrit.x = 400
gerrit.y = 550
gerrit.scale = 5
walkStage = 0
walkingLane = 0
hurtTime = 0
jump = False
jumpTime = 0
cooldown = 0

score = 0
warningsLeft = 1
goal = 20

walkingLane1X = 170
walkingLane2X = 300
walkingLane3X = 430

dummyProp = Actor("chicken")
dummyProp.x = -100
props = [dummyProp]

random.seed(time.time())

def on_mouse_down(pos, button):
    global startMenu, startButton, tutorialButton, tutorial, score, props, warningsLeft, jump, jumpTime, cooldown, lose, win, hurtTime
    if startButton.collidepoint(pos) and startMenu:
        startMenu = False
    elif tutorialButton.collidepoint(pos) and startMenu:
        tutorial = not tutorial
    elif quitButton.collidepoint(pos) and startMenu:
        pgzero.game.exit()
    elif backButton.collidepoint(pos):
        score = 0
        startMenu = True
        props.clear()
        warningsLeft = 1
        jump = False
        jumpTime = 0
        cooldown = 0
        lose = False
        win = False
        hurtTime = 0

holdingLeft = False
holdingRight = False

def update():
    global gerrit, walkStage, lastUpdate, score, goal, walkingLane, holdingLeft, holdingRight, hurtTime, homeScreenAnimation, win, lose, warningsLeft, jump, jumpTime, cooldown

    if startMenu:
        if not lastUpdate > float(time.time()) - 0.15:
            homeScreenBackground.image = 'homescreen' + homeScreenAnimation.__str__()
            homeScreenBackground.scale = 12
            if homeScreenAnimation == 19:
                homeScreenAnimation = 0
            homeScreenAnimation += 1
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
    elif warningsLeft < 0:
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

    if keyboard.up:
        if cooldown == 0 and jumpTime == 0:
            jump = True
    ### end of keyboard handling ###

    for prop in props:
        prop.y += 5
        if prop.y > HEIGHT + prop.height:
            props.remove(prop)
            continue
        if prop.colliderect(gerrit) and not jump:
            if prop.image == 'chicken':
                if random.randint(1, 2) == 1:
                    score += 5
                else:
                    warningsLeft -= 1
            elif prop.image == 'porridge':
                score += 2
            elif prop.image == 'scheepsbeschuit':
                score += 1
            elif prop.image == "crate":
                lose = True
                continue
            elif prop.image == "cow":
                lose = True
                continue
            elif prop.image == "barrel":
                lose = True
                continue
            props.remove(prop)
        elif prop.y > HEIGHT  + prop.height:
            props.remove(prop)

        for prop1 in props:
            if prop1 == prop:
                continue
            if prop.colliderect(prop1):
                props.remove(prop)

    backGround.y += 5
    backGround1.y += 5
    if backGround.y == HEIGHT + HEIGHT / 2:
        backGround.y = HEIGHT / 2 - HEIGHT
    if backGround1.y == HEIGHT + HEIGHT / 2:
        backGround1.y = HEIGHT / 2 - HEIGHT


    if not lastUpdate > float(time.time()) - 0.05: # main game loop runs less frequent
        if random.randint(0, 200) == 1:
            newprop = Actor("chicken")
            newprop.y = -200
            newprop.x = random.choice([walkingLane1X, walkingLane2X, walkingLane3X])
            newprop.scale = 5
            props.append(newprop)
        elif random.randint(0, 150) == 1:
            newprop = Actor("porridge")
            newprop.y = -200
            newprop.x = random.choice([walkingLane1X, walkingLane2X, walkingLane3X])
            newprop.scale = 5
            props.append(newprop)
        elif random.randint(0, 75) == 1:
            newprop = Actor("scheepsbeschuit")
            newprop.y = -200
            newprop.x = random.choice([walkingLane1X, walkingLane2X, walkingLane3X])
            newprop.scale = 5
            props.append(newprop)
        elif random.randint(0, 150) == 1:
            newprop = Actor("crate")
            newprop.y = -200
            newprop.x = random.choice([walkingLane1X, walkingLane2X, walkingLane3X])
            newprop.scale = 4
            props.append(newprop)
        elif random.randint(0, 120) == 1:
            newprop = Actor("cow")
            newprop.y = -200
            newprop.x = random.choice([walkingLane1X, walkingLane2X, walkingLane3X])
            newprop.scale = 6.5
            props.append(newprop)
        elif random.randint(0, 100) == 1:
            newprop = Actor("barrel")
            newprop.y = -200
            newprop.x = random.choice([walkingLane1X, walkingLane2X, walkingLane3X])
            newprop.scale = 6.5
            props.append(newprop)
        if hurtTime == 3:
            hurtTime = 0
        elif hurtTime > 0:
            hurtTime += 1
        else:
            if jump:
                jumpTime += 1
                gerrit.image = 'jump'
                gerrit.scale = 7
                if jumpTime == 25:
                    jump = False
                    jumpTime = 0
                    cooldown = 10
            else:
                if not cooldown == 0:
                    cooldown -= 1
                if not walkStage == 8:
                    gerrit.image = 'walk' + walkStage.__str__()
                    gerrit.scale = 5
                    walkStage += 1
                else:
                    gerrit.image = 'walk0'
                    gerrit.scale = 5
                    walkStage = 1

            if walkingLane == 0:
                gerrit.x = walkingLane1X
            elif walkingLane == 1:
                gerrit.x = walkingLane2X
            elif walkingLane == 2:
                gerrit.x = walkingLane3X

        lastUpdate = time.time()


def draw():
    global score, goal, lose, win

    backGround.draw()
    backGround1.draw()
    for prop in props:
        prop.draw()

    if tutorial:
        screen.fill((103, 190, 217))
        screen.draw.text(
            'In this game you play as Gerrit, a crewmate.\n'
            'To survive he needs to eat, but that\'s not easy...\n'
            '\n'
            'There is 3 types of food Gerrit can find and eat:\n'
            '\n'
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
        homeScreenBackground.draw()
        screen.draw.text(
            'Ship Runner',
            (180, 160),
            color=(0, 0, 0),
            fontsize=60
        )
        startButton.draw()
        tutorialButton.draw()
        quitButton.draw()

    elif win:
        screen.draw.text(
            'You survived the journey!',
            center=(WIDTH / 2, HEIGHT / 2),
            color=(0, 255, 0),
            fontsize=60
        )
        screen.draw.text(
            'Score: ' + str(score) + '/' + goal.__str__(),
            (15, 10), color=(255, 255, 255),
            fontsize=30
        )
        backButton.draw()
    elif lose:
        screen.draw.text(
            'You lost',
            center=(WIDTH / 2, HEIGHT / 2),
            color=(255, 0, 0),
            fontsize=60
        )
        backButton.draw()
    else:
        gerrit.draw()
        screen.draw.text(
            'Score: ' + str(score) + '/' + goal.__str__(),
            (15, 10), color=(255, 255, 255),
            fontsize=30
        )
        screen.draw.text(
            'Warnings left: ' + str(warningsLeft),
            (15, 30), color=(255, 255, 255),
            fontsize=30
        )


pgzrun.go() # Moet de laatste regel zijn