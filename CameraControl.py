import cv2
import Platform_Detection as PD
import numpy as np
import threading
import copy
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

def Showframe(frame, windowname = "USB Camera"):
    cv2.imshow(windowname, frame)

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

def ToGrayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def ToBlackWhite(frame,middleVal=128):
    return cv2.threshold(ToGrayscale(frame), middleVal, 255, cv2.THRESH_BINARY)[1]

def SetResolution(capture,W,H):
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, W)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, H)
    if capture.get(cv2.CAP_PROP_FRAME_WIDTH) == W and capture.get(cv2.CAP_PROP_FRAME_HEIGHT)== H:
        return True
    return False

class FrameCapture:

  def __init__(self, cap):
    self.Capture = cap
    self.LFrame = UpdateFrame(cap)
    self.Thread = threading.Thread(target=self.Updater, name="UserThread")
    self.Thread.start()


  def getLFrame(self):
      return copy.deepcopy(self.LFrame)

  # read frames as soon as they are available, keeping only most recent one
  def Updater(self):
    while True:
      self.LFrame = UpdateFrame(self.Capture)



