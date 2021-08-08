#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 8    // Digital pin connected to the DHT sensor 
#define DHTTYPE    DHT11     // DHT 11
DHT_Unified dht(DHTPIN, DHTTYPE);
uint32_t delayMS; 

const int MOTOR_RIGHT = 1;
const int MR_CONTROL_PIN_A = A0;
const int MR_CONTROL_PIN_B = A1;

const int ledPin = 13;    // the pin that the LED is attached to
int incomingByte;      // a variable to read incoming serial data into
int val;

void setup() {
  	Serial.begin(9600);		// Initialize device.

	dht.begin();	// Initialize DHT11 sensor
	sensor_t sensor;
	dht.temperature().getSensor(&sensor);
  	dht.humidity().getSensor(&sensor);
	delayMS = sensor.min_delay / 1000;

  	pinMode(MR_CONTROL_PIN_A,OUTPUT);	// Configure pin for motor to give output
  	pinMode(MR_CONTROL_PIN_B,OUTPUT);

	pinMode(ledPin, OUTPUT); 	// Configure pin for LED to give output
}

void loop() {

	// see if there's incoming serial data:
  	if (Serial.available() > 0) 
  	{
		incomingByte = Serial.read(); 	// read the oldest byte in the serial buffer:
		
		if (incomingByte == 'H') 		// if it's a capital H (ASCII 72), turn on the LED:
	  	{
		  	digitalWrite(ledPin, HIGH);
		  	forward(MOTOR_RIGHT); 
    	}

		if (incomingByte == 'L') 	// if it's an L (ASCII 76) turn off the LED:
		{
      		digitalWrite(ledPin, LOW);
      		stopMotor(MOTOR_RIGHT); 
    	}

    	if (incomingByte == 'R') 
		{
      		digitalWrite(ledPin, HIGH);
      		reverse(MOTOR_RIGHT); 
    	}
  	}
    
  	Serial.println();
  
  	delay(delayMS);   // Delay between measurements.
  	sensors_event_t event;      
  	dht.temperature().getEvent(&event);   // Get temperature event and print its value.

  	if (isnan(event.temperature)) {
    	Serial.println(F("Error reading temperature!"));
  	}

  	else 
	{
		Serial.print(F("Temperature: "));
    	Serial.print(event.temperature);
     	Serial.println(F("°C"));
     
     	if(event.temperature >= 40.00)
     	{
      		stopMotor(MOTOR_RIGHT);
      		val = digitalRead(DHTPIN);
      		Serial.write(val);
      		Serial.print(val);
      		while(1)
      		{}
     	}
    }

  	dht.humidity().getEvent(&event);      // Get humidity event and print its value.

  	if (isnan(event.relative_humidity)) {
    	Serial.println(F("Error reading humidity!"));
  	}
  	else 
	{
     	Serial.print(F("Humidity: "));
     	Serial.print(event.relative_humidity);
     	Serial.println(F("%"));
  	}

}

void forward( int motorNo)
{
  	switch (motorNo)
   	{
      	case MOTOR_RIGHT :
           	digitalWrite(MR_CONTROL_PIN_A, HIGH);
           	digitalWrite(MR_CONTROL_PIN_B, LOW);
           	break;

      	default:
		  	Serial.print("\r\n ERROR : Invalid motor no :");
      		Serial.print(motorNo);
   	}
}

/////////////////////////////////////////////////////////////////////

void reverse(int motorNo)
{
	switch (motorNo)
   	{
    	case MOTOR_RIGHT :
			digitalWrite(MR_CONTROL_PIN_A, LOW);
           	digitalWrite(MR_CONTROL_PIN_B, HIGH);
           	break;
		
		default:
			Serial.print("\r\n ERROR : Invalid motor no :");
      		Serial.print(motorNo);
    }
}

/////////////////////////////////////////////////////////////////////////

void stopMotor(int motorNo)
{
	switch (motorNo)
   	{
      	case MOTOR_RIGHT :
		  	digitalWrite(MR_CONTROL_PIN_A, LOW);
           	digitalWrite(MR_CONTROL_PIN_B, LOW);
           	break;
			   
		default: 
			Serial.print("\r\n ERROR : Invalid motor no :");
      		Serial.print(motorNo);
    }
}
