import cv2 as cv
import numpy as np

img = cv.imread('Adventure_full.png',0)

template_list = ['Adventure_button.png', 'ruin_5_icon.png', 'start_button.png', 'end_turn_button.png']

for i in range(len(template_list)):
    template = cv.imread(template_list[i], 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img, template,cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        print(pt)
        cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), (255,0,255), 2)
    if (np.any(res >= threshold)) == True:
        print("There is a MATCH!!!! ", template_list[i])
        print(pt, (pt[0] + w, pt[1] + h))
        print(int(pt[0]+w/2), int(pt[1]+h/2))
        break
    if (np.any(res >= threshold)) == False:
        print("There is no match ", template_list[i])
    #cv.imwrite('res_3.png',img)