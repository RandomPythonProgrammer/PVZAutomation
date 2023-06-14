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


def doTasks(tasks):
    for tool, popup in tasks:
        tool_pos = getPosition(tool)
        if tool_pos is not None:
            for popup_pos in getPositions(popup):
                pyautogui.click(*tool_pos)
                pyautogui.moveTo(*popup_pos)
                pyautogui.click()


def clickThings(things):
    for thing in things:
        thing_poses = getPositions(thing)
        for thing_pos in thing_poses:
            pyautogui.click(*thing_pos)


def manageGarden():
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


def main():
    process = multiprocessing.Process(target=manageGarden)
    process.start()
    while not keyboard.is_pressed('q'):
        pass
    process.terminate()


if __name__ == '__main__':
    main()
