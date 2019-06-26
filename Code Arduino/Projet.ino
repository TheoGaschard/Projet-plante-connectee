/*
 Program for the "projet plante conectée".



 */

#include <DHT.h> // Add of the DHT library.
#include <DHT_U.h> // Add of the DHT_U library.
#include <WiFi.h>
#include <ThingerWifi.h> // Adding the wi-fi library.
#include "Wire.h"
#include <Sparkfun_APDS9301_Library.h> // Adding the light sensor library.

#define _DEBUG_
#define _DISABLE_TLS_
#define THINGER_USE_STATIC_MEMORY
#define THINGER_STATIC_MEMORY_SIZE 512

#define MOISTURE_PIN A4 //PIN connected to the SEN0193 sensor.
#define DHTPIN A2 // PIN connected to the DHT11 sensor.
#define LIGHT_PIN 2 // Pin linked to the APDS9301 light sensor.

// We define the connection options.
#define USERNAME "username"
#define DEVICE_ID "arduino"
#define DEVICE_CREDENTIAL "r5Boe1Ige&#j"
#define SSID "XperiaXA2" // Name of the wi-fi network.
#define SSID_PASSWORD "123456" // Password of the wi-fi network.

ThingerWifi thing(USERNAME, DEVICE_ID, DEVICE_CREDENTIAL); // Establishing connection with the wi-fi network.

APDS9301 apds;


int moistureValue = 0;
int humidityValue = 0;  
int temperatureValue = 0;
int luminosityValue = 0;

DHT dht(DHTPIN, DHT11);


void setup(){
  
  pinMode(MOISTURE_PIN, INPUT);
  
  dht.begin();
  
  thing.add_wifi(SSID, SSID_PASSWORD); // Configure the wi-fi network.

  delay(50); // The CCS811 wants a brief delay after startup.
  Serial.begin(115200); // Open the serial monitor.
  Wire.begin();

  // APDS9301 sensor setup.
  apds.begin(0x39); 
  apds.setLowThreshold(0); // Sets the low threshold to 0, effectively
  //  disabling the low side interrupt.
  apds.setHighThreshold(50); // Sets the high threshold to 500. This
  //  is an arbitrary number I pulled out of thin
  //  air for purposes of the example. When the CH0
  //  reading exceeds this level, an interrupt will
  //  be issued on the INT pin.
  apds.enableInterrupt(APDS9301::INT_ON); // Enable the interrupt.
  apds.clearIntFlag();

  // Interrupt setup.
  pinMode(LIGHT_PIN, INPUT_PULLUP);
  Serial.println(apds.getLowThreshold());
  Serial.println(apds.getHighThreshold());

  thing["humidity"] >> humidityValue;
  thing["moisture"] >> moistureValue;
  thing["temperature"] >> temperatureValue;
  thing["luminosity"] >> luminosityValue;

}


void loop()
{
  moistureValue = analogRead(MOISTURE_PIN); // We collect the moisture of the dirt.
  humidityValue = dht.readHumidity(); // We collect the humidity of the air.
  temperatureValue = dht.readTemperature(); // We collect the temperature of the air.
  luminosityValue = apds.readCH0Level(); // We collect the luminosity.
  
  thing.handle();
  apds.clearIntFlag();
  delay(1000);


}
