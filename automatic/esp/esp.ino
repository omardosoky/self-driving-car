 #include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define ENA   14          // Enable/speed motors Right        GPIO14(D5)
#define ENB   12          // Enable/speed motors Left         GPIO12(D6)
#define IN_1  15          // L298N in1 motors Rightx          GPIO15(D8)
#define IN_2  13          // L298N in2 motors Right           GPIO13(D7)
#define IN_3  2           // L298N in3 motors Left            GPIO2(D4)
#define IN_4  0           // L298N in4 motors Left            GPIO0(D3)
#define TRIG  5           // Ultrasound Trig pin              GPIO5(D1)
#define ECHO  16          // Ultrasound Echo pin              GPIO16(D0)
#define SPEED 90         // Car speed
#define SPEEDR 100
#define WIFI_SSID "Galaxy Note10+"
#define WIFI_PASS "88888888"

long duration; // variable for the duration of sound wave travel
int distance; // variable for the distance measurement
String payload;  
int httpCode;
HTTPClient http;  //Declare an object of class HTTPClien
String url ="http://192.168.120.88:5635/direction";

void forward(){
      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      analogWrite(ENA, SPEED);
      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
      analogWrite(ENB, SPEED);
}
void backward(){
      digitalWrite(IN_1, HIGH);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, SPEED);
      digitalWrite(IN_3, HIGH);
      digitalWrite(IN_4, LOW);
      analogWrite(ENB, SPEED);
}
void right(){
      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, HIGH);
      analogWrite(ENA, SPEEDR);
      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, LOW);
      analogWrite(ENB, SPEEDR);
}
void left(){
      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, SPEEDR);
      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, HIGH);
      analogWrite(ENB, SPEEDR);
}
void stopM(){
      digitalWrite(IN_1, LOW);
      digitalWrite(IN_2, LOW);
      analogWrite(ENA, SPEED);
      digitalWrite(IN_3, LOW);
      digitalWrite(IN_4, LOW);
      analogWrite(ENB, SPEED);
}

void setup(){
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);  
  pinMode(IN_1, OUTPUT);
  pinMode(IN_2, OUTPUT);
  pinMode(IN_3, OUTPUT);
  pinMode(IN_4, OUTPUT); 
  pinMode(TRIG,OUTPUT);
  pinMode(ECHO,INPUT); 
  
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASS); 
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting");
    delay(100);
  }
}

void loop(){
  // Clears the trigPin condition
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(ECHO, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  // Displays the distance on the Serial Monitor
  Serial.println("distance is "+ String(distance));
  if(distance<10){
    stopM();
  }
  else{
    if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
      WiFiClient wifi;
      http.begin(wifi,url); //Specify request destination
      httpCode = http.GET(); //Send the request
      if (httpCode > 0) { //Check the returning code
        payload = http.getString();   //Get the request response payload
      }else //Serial.println("HTTP Failed");
      http.end();   //Close connection
    }
    if(payload == "0"){
      Serial.println("forward");
      forward();
    }else if(payload == "1"){
      Serial.println("right");
      right();
    }
    else if(payload == "2"){
      Serial.println("left");
      left();
    }
  }
  delay(500);
  stopM();
  delay(500);
}
