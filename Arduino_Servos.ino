#include <Servo.h>
#include <math.h>

String s1, s2; 
String var;
Servo servo1, servo2;     // create servo object to control a servo
String strings[2];
int pos = 0;              // variable to store the servo position


// This function splits a given string into two strings seperated with with seperator 
String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void setup() { 
  Serial.begin(9600); //initialize serial COM at 9600 baudrate
  servo1.attach(9);
  servo2.attach(10);
  Serial.println("Hi!, I am Arduino");
  Serial.setTimeout(20);
  
}
 
void loop() {
if (Serial.available()){
  var = Serial.readString();
  if (var != "sweep"){ 
  String xval = getValue(var, '#', 0);
  String yval = getValue(var, '#', 1);
  servo1.write(atoi(xval.c_str()));
  servo2.write(atoi(yval.c_str()));
}
else{
  for (pos = 0; pos <= 180; pos += 1) {        // goes from 0 degrees to 180 degrees in steps of 1 degree
    if (Serial.readString() != "sweep") break;
    servo1.write(pos);
    servo2.write(pos);                // tell servo to go to position in variable 'pos'
    delay(200);                       // waits 200ms for the servo to reach the position   
    }
  for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    if (Serial.readString() != "sweep") break;
    servo1.write(pos);
    servo2.write(pos);// tell servo to go to position in variable 'pos'
    delay(200);                       // waits 200ms for the servo to reach the position
    }
  }
}
}
