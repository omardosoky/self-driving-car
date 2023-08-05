#include<SoftwareSerial.h>
#define echoPin 2 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 3 //attach pin D3 Arduino to pin Trig of HC-SR04
long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement
int izqA = 9; 
int izqB = 10; 
int derA = 11; 
int derB = 12; 
int vel = 255; // Velocidad de los motores (0-255)
char dir ='0';
void setup(){
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
  pinMode(derA, OUTPUT);
  pinMode(derB, OUTPUT);
  pinMode(izqA, OUTPUT);
  pinMode(izqB, OUTPUT);
  analogWrite(derB, 0); 
      analogWrite(izqB, 0); 
      analogWrite(derA, 100); 
      analogWrite(izqA, 200);
}
void loop(){
  if(Serial.available() >0){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)

  if(distance <20){
      analogWrite(derB, 0); 
      analogWrite(izqB, 0); 
      analogWrite(derA, 0); 
      analogWrite(izqA, 0); 
  }
  else{
    dir = Serial.read();
    Serial.print("direction is");
    Serial.println(dir);
    //forward
    if(dir =='0'){
      analogWrite(derB, 0); 
      analogWrite(izqB, 0); 
      analogWrite(derA, vel); 
      analogWrite(izqA, vel); 
    }
    //right
    else if(dir =='1'){
      analogWrite(derB, 0); 
      analogWrite(izqB, 0); 
      analogWrite(derA, 100); 
      analogWrite(izqA, 200); 
    }
    //left
    else if (dir == '2')
    {
      analogWrite(derB, 0); 
      analogWrite(izqB, 0);
      analogWrite(izqA, 100);
      analogWrite(derA, 200); 
    }
    //stop
    else{
      analogWrite(derB, 0); 
      analogWrite(izqB, 0); 
      analogWrite(derA, 0); 
      analogWrite(izqA, 0); 
    }
  }
  }
  }
  
