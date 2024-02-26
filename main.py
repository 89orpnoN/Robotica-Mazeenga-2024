import Platform_Detection as PD
import threading
import CameraControl as CC
import cv2
import pytesseract
import asyncio #è una buona libreria per condividere informazioni tra threads


def MonitorYellow(cap):
    ifr = 0
    while True:
        Frame = CC.UpdateFrame(cap)
        yellow = [48, 131, 117]
        tollerance = 25
        mask = CC.RangeMask(Frame,yellow,tollerance)


        min_contour_area = 600

        contorni = CC.Contorni(mask,min_contour_area)
        contorno = CC.Contorno(mask, min_contour_area)

        BWframe = cv2.cvtColor(Frame, cv2.COLOR_BGR2GRAY)
        black_and_white = cv2.threshold(BWframe, 90, 255, cv2.THRESH_BINARY)[1]
        cv2.drawContours(Frame, contorni, -1, (0, 255, 0), 3)

        if ifr == 30:
            print(pytesseract.image_to_string(Frame,config=("-c tessedit"
                  "_char_whitelist=HSU"
                  " --psm 10"
                  " -l osd"
                  " ")))
            ifr = 0


        x, y, w, h = cv2.boundingRect(contorno)
        cv2.rectangle(Frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.imshow('Colored Squares Detection', Frame)
        cv2.imshow('bLACK AND WITE', BWframe)
        cv2.imshow('NO GRAYSCALE', black_and_white)
        ifr += 1



cap = CC.NewCapture(0)

desired_width = 1280
desired_height = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print(f"Actual Resolution: {actual_width}x{actual_height}")

threading.Thread(target=MonitorYellow,args=[cap]).start()
if cv2.waitKey(1) & 0xFF == ord('q'):
    cv2.destroyAllWindows()