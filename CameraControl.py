import cv2
import Platform_Detection as PD
import numpy as np
def NewCapture(Cam):
    cap = PD.DoThisOnPlatform("Windows", cv2.VideoCapture, [Cam, cv2.CAP_DSHOW], cv2.VideoCapture, [Cam])[1]
    return cap
def ShowCapture(cap):
    while True:

        Showframe(UpdateFrame(cap))

    cap.release()
    cv2.destroyAllWindows()

def UpdateFrame(cap):
    # Read a frame from the camera
    ret, frame = cap.read()

    # Check if the frame was read successfully
    if not ret:
        raise Exception("Impossibile estrarre frame")
    return frame

def Showframe(frame):
    cv2.imshow("USB Camera", frame)

def RangeMask(frame,color,tollerance):
    ColorLow = np.array(color) - tollerance
    ColorHigh = np.array(color) + tollerance
    mask = cv2.inRange(frame, ColorLow, ColorHigh)
    return mask

def Contorni(mask, minArea = 0): #trova tutti i contorni che rispettano le condizioni
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)[0]
    valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > minArea]
    return valid_contours
def Contorno(mask,minArea = 0): #trova il contorno più grande

    MaxArea = minArea
    Contorno = None

    Contorni = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)[0]

    for i in Contorni:
        area = cv2.contourArea(i)
        if area > MaxArea:
            MaxArea = area
            Contorno = i

    return Contorno
