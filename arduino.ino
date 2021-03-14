#include <Servo.h>
#include <LiquidCrystal.h>
LiquidCrystal lcd (7,6,5,4,3,2);
Servo servoMotor;

const int pinLED1 = 8;
const int pinLED2 = 9;
const int pinSERVO = 10;

void setup() 
{
   Serial.begin(9600);
   lcd.begin(16,2);
   pinMode(pinLED1, OUTPUT);
   pinMode(pinLED2, OUTPUT);
   servoMotor.attach(pinSERVO);
   servoMotor.write(0);
   lcd.clear();
}
 
void loop()
{
   if (Serial.available()>0) 
   {
      char option = Serial.read();
      if (option == '1')
      {
         acceder();
      }
      else
      {
        if(option == '0')
        {
          no_acceder();    
        }
        else{
          if(option== '2')
          {
            deteccion();
          }
        }
      }
   }
}

void deteccion(){
  lcd.clear();
  lcd.setCursor(3,0);
  lcd.print("Detectando");
  lcd.setCursor(3,1);
  lcd.print("Mascarilla");
}

void acceder(){
  servoMotor.write(150);
  digitalWrite(pinLED1, HIGH);
  digitalWrite(pinLED2, LOW);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Acceso Permitido");
  lcd.setCursor(6,1);
  lcd.print("Siga");
  delay(4200);
}

void no_acceder(){
  servoMotor.write(0);
  digitalWrite(pinLED1, LOW);
  digitalWrite(pinLED2, HIGH);
  lcd.clear();  
  lcd.setCursor(0,0);
  lcd.print("Acceso Denegado");
  lcd.setCursor(0,1);
  lcd.print("Verif. Tapabocas");
}
