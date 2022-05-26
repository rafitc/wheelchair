"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
import serial as foo
import cv2
from gaze_tracking import GazeTracking
import time 

serial_port = "/dev/tty.usbserial-1420"
arduino = foo.Serial(port=serial_port, baudrate=9600)

gaze = GazeTracking()
webcam = cv2.VideoCapture(1)

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""
    
    k = gaze.horizontal_ratio()
    if k == None:
        print("GOT NONE")
        k = 0.0

    print("Horizont ratio : ",k)
    if gaze.is_blinking():
        text = "Blinking"
        arduino.write(bytes("4", 'utf-8'))
        
    if gaze.is_right():
        arduino.write(bytes("2", 'utf-8'))
        text = "Looking right"
        time.sleep(0.3)
    if gaze.is_left():
        arduino.write(bytes("3", 'utf-8'))
        text = "Looking left"
        time.sleep(0.3)
    # if gaze.is_center():
    #     arduino.write(bytes("1", 'utf-8'))
    #     text = "Looking center"
    #     time.sleep(0.3)
    if k >= 0.50 and k<=0.55:
        text = "Looking center"
        arduino.write(bytes("1", 'utf-8'))
        time.sleep(0.3)
        print("center")
    else:
        arduino.write(bytes("4", 'utf-8'))

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break
   
webcam.release()
cv2.destroyAllWindows()
