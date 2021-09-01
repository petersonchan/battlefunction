from ppadb.client import Client
import cv2 as cv
import numpy as np
import time
import os

zeroManaCardList = ['skill_twinNeedle_0_46_0.png','skill_vineDagger_0_31_46.png','skill_allOutShot_0_186_0.png']
skill_list = ['skill_crimsonWater_1_186_46.png', \
              'skill_allOutShot_0_186_0.png', \
              'skill_eggbomb_1_186_0.png', \
              'skill_grubSurprise_1_155_77.png', \
              'skill_riskyFeather_1_232_0.png', \
              'skill_tinyCatapult_1_124_62.png', \
              'skill_swallow_1_124_46.png', \
              'skill_turnipRocket_1_93_124.png', \
              'skill_shroomsGrace_1_0_62.png', \
              'skill_darkSwoop_1_38_0.png', \
              'skill_twinNeedle_0_46_0.png', \
              'skill_vineDagger_0_31_46.png']

move_list = ['move_0-10.png', \
             'move_1-10.png', \
             'move_2-10.png', \
             'move_3-10.png', \
             'move_4-10.png', \
             'move_5-10.png', \
             'move_6-10.png', \
             'move_7-10.png', \
             'move_8-10.png', \
             ]

def connect_device():
    adb = Client(host='127.0.0.1',port=5037)
    devices = adb.devices()
    if len(devices) == 0:
        print("No Devices Attached")
        quit()
    else:
        print("Device Connected")
    return devices[0]

def take_screenshot(device, screen_name):
    image = device.screencap()
    with open(screen_name, 'wb') as f:
        f.write(image)

def clickSrceen(x_position, y_position):
    adb_command = "adb shell input tap " + str(x_position) + " " + str(y_position)
    os.system(adb_command)

def dragAndDropCard(x_position, y_position):
    adb_command = "adb shell input draganddrop " + str(x_position) + " " + \
                  str(y_position) + " " + str(x_position) + " " + str(y_position + 230)
    os.system(adb_command)

def zeroManaCardOnHand(screen_path):
    collector = []
    img = cv.imread(screen_path, 0)
    for i in range(len(zeroManaCardList)):
        template = cv.imread(zeroManaCardList[i], 0)
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.9
        if np.any(res >= threshold):
            loc = list(np.where(res >= threshold))
            for pt in (zip(*loc[::-1])):
                collector.append([zeroManaCardList[i], pt[0], pt[1]])
    return collector

def moveRemaining(screen_path):
    img = cv.imread(screen_path, 0)
    for i in range(len(move_list)):
        template = cv.imread(move_list[i], 0)
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.9
        if np.any(res >= threshold):
            return i

def allSkillOnHand(screen_path):
    collector = []
    img = cv.imread(screen_path, 0)
    for i in range(len(skill_list)):
        template = cv.imread(skill_list[i], 0)
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.9
        if np.any(res >= threshold):
            loc = list(np.where(res >= threshold))
            for pt in (zip(*loc[::-1])):
                collector.append([skill_list[i], pt[0], pt[1]])
    return collector

def isEndTurnButtonExist(screen_path):
    img = cv.imread(screen_path,0)
    template = cv.imread('end_turn_button.png', 0)
    res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    return np.any(res >= threshold)

def isStartButtonExist(screen_path):
    img = cv.imread(screen_path,0)
    template = cv.imread('start_button.png', 0)
    res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    return np.any(res >= threshold)

def isVictoryImageExist(screen_path):
    img = cv.imread(screen_path,0)
    threshold = 0.8
    template_1 = cv.imread('victory_check_1.png', 0)
    res_1 = cv.matchTemplate(img, template_1, cv.TM_CCOEFF_NORMED)
    template_2 = cv.imread('victory_check_2.png', 0)
    res_2 = cv.matchTemplate(img, template_2, cv.TM_CCOEFF_NORMED)
    return (np.any(res_1 >= threshold) or np.any(res_2 >= threshold))

def isDefeatedImageExist():
    img = cv.imread(screen_path,0)
    threshold = 0.8
    template_1 = cv.imread('defected_check_1.png', 0)
    res_1 = cv.matchTemplate(img, template_1, cv.TM_CCOEFF_NORMED)
    template_2 = cv.imread('defected_check_2.png', 0)
    res_2 = cv.matchTemplate(img, template_2, cv.TM_CCOEFF_NORMED)
    return (np.any(res_1 >= threshold) or np.any(res_2 >= threshold))

def battleStage(device_phone, end_turn_button_x_position, end_turn_button_y_position):
    battleFunctionSwitch = True
    previouDragDropPositionX = 0
    previouDragDropPositionY = 0
    while battleFunctionSwitch == True:
        take_screenshot(device_phone, 'screen.png')
        if isEndTurnButtonExist('screen.png') == True:
            if len(allSkillOnHand('screen.png')) == 0:
                clickSrceen(end_turn_button_x_position, end_turn_button_y_position)
            else: #Have card(s) on hard
                if moveRemaining('screen.png') == 0:
                    if len(zeroManaCardOnHand('screen.png')) == 0:
                        clickSrceen(end_turn_button_x_position, end_turn_button_y_position)
                    elif len(zeroManaCardOnHand('screen.png')) != 0:
                        cardToDragAndDrop = zeroManaCardOnHand('screen.png')[0]
                        if cardToDragAndDrop[1] == previouDragDropPositionX and cardToDragAndDrop[2] == previouDragDropPositionY:
                            clickSrceen(end_turn_button_x_position, end_turn_button_y_position)
                        dragAndDropCard(cardToDragAndDrop[1], cardToDragAndDrop[2])
                        previouDragDropPositionX = cardToDragAndDrop[1]
                        previouDragDropPositionY = cardToDragAndDrop[1]
                        time.sleep(1)
                elif moveRemaining('screen.png') != 0:
                    cardToDragAndDrop = allSkillOnHand('screen.png')[0]
                    if cardToDragAndDrop[1] == previouDragDropPositionX and cardToDragAndDrop[2] == previouDragDropPositionY:
                        clickSrceen(end_turn_button_x_position,end_turn_button_y_position)
                    dragAndDropCard(cardToDragAndDrop[1],cardToDragAndDrop[2])
                    previouDragDropPositionX = cardToDragAndDrop[1]
                    previouDragDropPositionY = cardToDragAndDrop[1]
                    time.sleep(1)
        elif isEndTurnButtonExist('screen.png') == False:
            if isVictoryImageExist('screen.png') or isDefeatedImageExist('screen.png'):
                #End Battle
                clickSrceen(1000,1000)
                time.sleep(2)
                if isStartButtonExist('screen.png') == True:
                    battleFunctionSwitch = False
            else:
                #in battle animation
                print("in battle animation")
                continue
    print("END battle function")


def main():
    devicePhone = connect_device()
    take_screenshot(devicePhone, 'screen.png')
    if isEndTurnButtonExist('screen.png'):
        img = cv.imread('screen.png', 0)
        template = cv.imread('end_turn_button.png', 0)
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            if (np.any(res >= threshold)) == True:
                x_position = int(pt[0] + w / 2)
                y_position = int(pt[1] + h / 2)
        battleStage(devicePhone, x_position, y_position)

if __name__ == "__main__":
    main()


