from ppadb.client import Client
import keyboard
import cv2 as cv
import numpy as np
import time
import os
import test_battleFunction

def connect_device():
    adb = Client(host='127.0.0.1',port=5037)
    devices = adb.devices()
    if len(devices) == 0:
        print("No Devices Attached")
        quit()
    else:
        print("Device Connected")
    return devices[0]

def take_screenshot(device):
    image = device.screencap()
    with open('screen.png', 'wb') as f:
        f.write(image)



if __name__ == "__main__":
    device_phone = connect_device()
    #take_screenshot(device_phone)
    while True:
        screenImage = device_phone.screencap()
        take_screenshot(device_phone)
        img = cv.imread('screen.png', 0)
        template_list = ['Adventure_button.png', 'ruin_5_icon.png', 'start_button.png', 'end_turn_button.png']
        for i in range(len(template_list)):
            template = cv.imread(template_list[i], 0)
            w, h = template.shape[::-1]
            res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                #cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (255, 0, 255), 2)
                if (np.any(res >= threshold)) == True:
                    print("There is a MATCH!!!! ", template_list[i])
                    print(pt, (pt[0] + w, pt[1] + h))
                    tap_x_position = int(pt[0] + w / 2)
                    tap_y_position = int(pt[1] + h / 2)
                    print("Centre point: ", tap_x_position, tap_y_position)
                    if template_list[i] != 'end_turn_button.png' :
                        adb_command = "adb shell input tap " + str(tap_x_position) + " " + str(tap_y_position)
                        os.system(adb_command)
                        time.sleep(2)
                    if template_list[i] == 'end_turn_button.png':
                        print("Battle function!!!")
                        test_battleFunction.main()
                        time.sleep(2)
                    break
                if (np.any(res >= threshold)) == False:
                    print("There is no match ", template_list[i])
                time.sleep(2)


