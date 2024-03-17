from motors import robot
import threading

#script inutile fatto per diletto, utile per testare il movimento

last_button = [""]
before_last_button = [""]
mvm = 0
def checkbutton(last_button):
    while True:
        last_button[0] = input()
threading.Thread(target=checkbutton, args=[last_button], name="UserThread").start()
while True:
    if last_button[0] == "W"!= before_last_button[0]:
        mvm+=1
    elif last_button[0] == "S"!= before_last_button[0]:
        mvm -= 1
    if last_button[0] != before_last_button[0] and (last_button[0] == "S" or last_button[0] == "W"):
        if mvm == 1:
            robot.forward()
        elif mvm == 0:
            robot.stop()
        elif mvm == -1:
            robot.backward()
    if last_button[0] == "D":
        robot.right()
        mvm = 0
    elif last_button[0] == "A":
        robot.left()
        mvm = 0

    before_last_button[0] = last_button[0]

