import Platform_Detection as PD
import threading
import CameraControl as CC
import cv2
import numpy as np
# Open the video capture object

cap = CC.NewCapture(0)
#visione videocamera
#threading.Thread(target=CC.UpdateFrames,args=[cap]).start()

while True:
    Frame = CC.UpdateFrame(cap)
    yellow = [48, 131, 117]
    tollerance = 25
    mask = CC.RangeMask(Frame,yellow,tollerance)


    min_contour_area = 600

    contorni = CC.Contorni(mask,min_contour_area)
    contorno = CC.Contorno(mask, min_contour_area)

    cv2.drawContours(Frame, contorni, -1, (0, 255, 0), 3)


    x, y, w, h = cv2.boundingRect(contorno)
    cv2.rectangle(Frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow('Colored Squares Detection', Frame)


cv2.destroyAllWindows()