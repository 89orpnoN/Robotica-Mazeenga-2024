import Platform_Detection as PD
import threading
import CameraControl as CC
# Open the video capture object

cap = CC.NewCapture(0)

threading.Thread(target=CC.UpdateFrames,args=[cap]).start()

