import cv2
import imutils
import numpy as np
import serial
import time  # Required to use delay functions

class screen_shot:

    def __init__(self):
        self.refPt = []
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
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k % 256 == 32:
                # SPACE pressed
                # img_name = "source.jpg"
                # cv2.imwrite(img_name, frame)
                # print("{} written!".format(img_name))
                # img_counter += 1
                self.snap_shot = frame
                cv2.imwrite("snap.jpg", frame)
        cam.release()
        cv2.destroyAllWindows()

    def click_and_crop(self, event, x, y, flags, param):

        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being
        # performed
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
        #(y, x)
        while True:
            ret, img_rgb = cap.read()
            # img_rgb = cv2.imread("snap.jpg")
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

            template = cv2.imread('template.jpg', 0)
            w, h = template.shape[::-1]

            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            # loc = np.where(res >= threshold)
            (_, maxVal, _, locMax) = cv2.minMaxLoc(res)
            if maxVal > threshold:
                pt = locMax #(loc[1][0], loc[0][0])
                cenT = (pt[0]+w/2, pt[1]+h/2)
                cenF = (img_rgb.shape[0]/2, img_rgb.shape[1]/2)
                degX = int(cenT[0]/3.555)
                degY = int(cenT[1] / 2.666)
                print(maxVal, locMax)
                # arduino.write(((str(degX)+'#'+str(degY)).encode()))
                # time.sleep(0.05)
                # arduino.write((str(degY).encode()))
                # time.sleep(0.05)
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)
            else:
                print("No matches found")
                # arduino.write("sweep".encode())


            cv2.imshow("img", img_rgb)
            k = cv2.waitKey(1) & 0xFF
            if k == ord("q"):
                break


# arduino = serial.Serial('com19', 9600)  # Create Serial port object called arduinoSerialData
# time.sleep(2)  # wait for 2 secounds for the communication to get established
# print(arduino.readline()) # read the serial data and print it as line

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
