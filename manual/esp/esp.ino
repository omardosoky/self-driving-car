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
#define WIFI_SSID "STUDBME2"
#define WIFI_PASS "BME2Stud"


String payload;  
int httpCode;
HTTPClient http;  //Declare an object of class HTTPClien
String url ="http://172.28.131.51:5635/sendDirection";

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
    delay(100);
  }
}

void loop(){
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
    else if(payload == "3"){
      Serial.println("stop");
      stopM();
    }
    else if(payload == "5"){
      Serial.println("backward");
      backward();
    }
    else {
      Serial.println("None");
      stopM();
    }
    delay(100);
}
