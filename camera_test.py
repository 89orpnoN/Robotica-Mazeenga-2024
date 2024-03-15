import Platform_Detection as PD
import threading
import CameraControl as CC
import cv2
import pytesseract
import os
import time
import asyncio #è una buona libreria per condividere informazioni tra threads


def MonitorYellow(UpdatedFrames):
    epoch = time.process_time_ns()
    while True:
        Frame = UpdatedFrames.getLFrame()
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
        
        PD.DoThisOnPlatform("Windows",CC.Showframe,[Frame,'Colored Squares Detection'])

        print("colore: " + str((time.process_time_ns() - epoch) / 1000000 + "ms"))
        epoch = time.process_time_ns()

def ScanLetters(UpdatedFrames):
    #os.environ['TESSDATA_PREFIX'] = os.getcwd()+"/Tesseract OCR models"
    while True:
        epoch = time.process_time_ns()
        Frame = UpdatedFrames.getLFrame()
        Frame=CC.ToBlackWhite(Frame,90)
        print(pytesseract.image_to_string(Frame, config='--psm 10 -c tessedit_char_whitelist=HSsUu').lower())
        PD.DoThisOnPlatform("Windows",CC.Showframe,[Frame,'Letter'],print,["Lettere sta andando"])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        print("lettere: " + str((time.process_time_ns() - epoch) / 1000000 + "ms"))

def startCamering():
    cap = CC.NewCapture(0)
    cap.set(3, 160)
    cap.set(4, 120)

    cap2 = CC.NewCapture(2)
    cap2.set(3, 160)
    cap2.set(4, 120)

    UpdatedFrames = CC.FrameCapture(cap)
    UpdatedFrames2 = CC.FrameCapture(cap2)

    #threading.Thread(target=MonitorYellow,args=[UpdatedFrames],name="UserThread").start()
    threading.Thread(target=ScanLetters,args=[UpdatedFrames],name="UserThread").start()

    #threading.Thread(target=MonitorYellow, args=[UpdatedFrames2], name="UserThread").start()
    threading.Thread(target=ScanLetters, args=[UpdatedFrames2], name="UserThread").start()

    for t in threading.enumerate():
        if t.getName()=="UserThread":
            t.join()

startCamering()
