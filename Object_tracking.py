import cv2
import imutils
import numpy as np
import serial
import time  # Required to use delay functions

class screen_shot:

    def __init__(self):
        self.refPt = []      #reference point for cropping
        self.cropping = False
        self.snap_shot = None
        self.template = None

    def take_snap(self):
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("test")

        while True:
            ret, frame = cam.read()
            cv2.imshow("test", frame)
            if not ret:
                break
            k = cv2.waitKey(1)

            if k == ord("q"):
                # q pressed
                break
            elif k % 256 == 32:
                # SPACE pressed
                self.snap_shot = frame
                cv2.imwrite("snap.jpg", frame) #in case self.snap_shot was none
        cam.release()
        cv2.destroyAllWindows()

    def click_and_crop(self, event, x, y, flags, param):
        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being performed
        if event == cv2.EVENT_LBUTTONDOWN:
            self.refPt = [(x, y)]
            self.cropping = True

        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished
            self.refPt.append((x, y))
            self.cropping = False

            # draw a rectangle around the region of interest
            cv2.rectangle(img_rgb, self.refPt[0], self.refPt[1], (0, 255, 0), 2)
            cv2.imshow("image", img_rgb)


    def crop(self):
        while True:
            # display the image and wait for a keypress
            cv2.imshow("image", img_rgb)
            key = cv2.waitKey(1) & 0xFF

            # if the 'r' key is pressed, reset the cropping region
            if key == ord("r"):
                image = clone.copy()

            # if the 'c' key is pressed, break from the loop
            elif key == ord("c"):
                break

    def match(self):
        cap = cv2.VideoCapture(0)
        #Note that cv2 saves coordiantes in (y, x) order
        while True:
            ret, img_rgb = cap.read()
            # img_rgb = cv2.imread("snap.jpg") #in case self.snap_shot was empty
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

            template = cv2.imread('template.jpg', 0)
            w, h = template.shape[::-1]

            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8    #Threshold can be changed
            (_, maxVal, _, locMax) = cv2.minMaxLoc(res)            #saves the best match
            if maxVal > threshold:
                cenT = (locMax[0]+w/2, locMax[1]+h/2)              #Center of template
                cenF = (img_rgb.shape[0]/2, img_rgb.shape[1]/2)    #Center of image
                degX = int(cenT[0]/3.555)                          #mapping 640 pixel into 180 degrees
                degY = int(cenT[1] / 2.666)                        #mapping 480 pixel into 180 degrees
                print(maxVal, locMax)
                arduino.write(((str(degX)+'#'+str(degY)).encode()))
                time.sleep(0.05)                                   #This delay is requierd so the arduino does not miss any data
                arduino.write((str(degY).encode()))
                time.sleep(0.05)
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)
            else:
                print("No matches found")
                arduino.write("sweep".encode())


            cv2.imshow("img", img_rgb)
            k = cv2.waitKey(1) & 0xFF
            if k == ord("q"):
                break

#Setting up Serial connection 
arduino = serial.Serial('com19', 9600)  # Create Serial port object called arduino // serial port name "com19" should be changed to match the arduino
time.sleep(2)  # wait for 2 secounds for the communication to get established
print(arduino.readline()) # read the serial data and print it as line #To make sure that serial connections was established correctly 

obj = screen_shot()
obj.take_snap()
img_rgb = obj.snap_shot
clone = img_rgb.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", obj.click_and_crop)
obj.crop()

if len(obj.refPt) == 2:
    roi = clone[obj.refPt[0][1]:obj.refPt[1][1], obj.refPt[0][0]:obj.refPt[1][0]]
    cv2.imwrite("template.jpg", roi)

cv2.destroyAllWindows()
obj.match()
cv2.destroyAllWindows()
exit()
