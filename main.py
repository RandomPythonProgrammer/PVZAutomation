import multiprocessing
import os
import time

import keyboard
import pyautogui

pyautogui.FAILSAFE = False


def getPositions(image):
    images = pyautogui.locateAllOnScreen(os.path.join('images', image), confidence=0.9)
    return [(image[0] + image[2] / 2, image[1] + image[3] / 2) for image in images]


def getPosition(image):
    image = pyautogui.locateOnScreen(os.path.join('images', image), confidence=0.9)
    return (image[0] + image[2] / 2, image[1] + image[3] / 2) if image is not None else None


def collides(rect, point):
    x, y, w, h = rect
    x_, y_ = point
    return x <= x_ <= x+w and y <= y_ <= y+h


def clickItem(image):
    position = getPosition(image)
    if position is not None:
        pyautogui.click(*position)


def buySupplies():
    clickItem('shop.png')
    goBack = None
    while goBack is None:
        clickItem('shop.png')
        goBack = getPosition('goBack.png')
    while getPosition('storeFertilizer.png') is not None:
        clickItem('storeFertilizer.png')
        while getPosition('yes.png') is not None:
            clickItem('yes.png')
    while getPosition('storeSpray.png') is not None:
        clickItem('storeSpray.png')
        while getPosition('yes.png') is not None:
            clickItem('yes.png')
    pyautogui.click(*goBack)


def doTasks(tasks):
    for tool, popup in tasks:
        tool_pos = getPosition(tool)
        if tool_pos is not None:
            for popup_pos in getPositions(popup):
                pyautogui.click(*tool_pos)
                pyautogui.moveTo(*popup_pos)
                pyautogui.mouseDown()
                time.sleep(0.1)
                pyautogui.mouseUp()


def clickThings(things):
    arrow = pyautogui.locateOnScreen(os.path.join('images', 'menu.png'), confidence=0.7)
    for thing in things:
        thing_poses = getPositions(thing)
        for thing_pos in thing_poses:
            if arrow is None or not collides(arrow, thing_pos):
                pyautogui.click(*thing_pos)


def manageGarden():
    lastBuy = time.time()
    lastSwap = time.time()
    while True:
        doTasks([
            ('waterCan.png', 'water.png'),
            ('sprayCan.png', 'spray.png'),
            ('musicPlayer.png', 'music.png'),
            ('fertilizerBag.png', 'fertilizer.png')
        ])
        start = time.time()
        while time.time() - start < 5:
            clickThings([
                'snail.png',
                'silverCoin.png',
                'goldCoin.png',
                'diamond.png'
            ])
        if time.time() - lastBuy > 60:
            buySupplies()
            lastBuy = time.time()
        if time.time() - lastSwap > 900:
            clickItem('arrow.png')
            lastSwap = time.time()
        if getPosition('tree.png') is not None or getPosition('tree1.png') is not None:
            clickItem('arrow.png')
            lastSwap = time.time()


def main():
    process = multiprocessing.Process(target=manageGarden)
    process.start()
    while not keyboard.is_pressed('q'):
        pass
    process.terminate()


if __name__ == '__main__':
    main()
