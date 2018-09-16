# Object_Tracking_Using_Python_and Arduino Uno

 
The objective of the robot is to continuously move so the detected object is in the center of the image.
The video is fed through a web cam mounted on the top of the robot with resolution of 480*640.
The coordinates of the center of the object x and y range from 0 to 640 and from 0 to 480 respectively which mapped into degrees sent to servos by deviding x by 3.55 and y by 2.66.
Python and OpenCV are used to let the user determine the object to be tracked, and detect the object using template matching concept.
