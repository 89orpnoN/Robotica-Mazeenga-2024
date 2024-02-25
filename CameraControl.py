import cv2
import Platform_Detection as PD
def NewCapture(Cam):
    cap = PD.DoThisOnPlatform("Windows", cv2.VideoCapture, [Cam, cv2.CAP_DSHOW], cv2.VideoCapture, [Cam])[1]
    return cap
def UpdateFrames(cap):
    while True:

        Showframe(UpdateFrame(cap))
        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

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