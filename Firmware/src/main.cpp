#include <WiFi.h>
#include <PubSubClient.h>
#include "BLEBeaconNotifier.h"
#include "HttpService.h"
// === Configuration Wi-Fi ===


// const char* ssid = "SM-G960W9028";
// const char* password = "imzh7060";
// Wifi settings
const char*     SSID = "Beans";
const char*     PASSWORD = "12345678";

// Time settings
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 2L * 60L * 60L;
const int   daylightOffset_sec = 3600; // Example for 1 hour daylight saving

WiFiClient wifiClient;
BLEBeaconNotifier Beacon;
HttpService httpService(wifiClient);

void setupWifi(){
  Serial.println();
  Serial.print("Connexion à ");
  Serial.println(SSID);
  WiFi.begin(SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer); // Configure date system
}


// === Setup initial ===
void setup() {
  Serial.begin(115200);
  delay(10);
  setupWifi();
  Beacon.setup();
  httpService.setup();
}

// === Boucle principale ===
void loop() {
  Beacon.loop();
  httpService.loop();
  // Filter by size
  for (size_t i = 0; i < Beacon.Entries.size();) { // Send notifications for entries
    if (httpService.sendEnterPacket(Beacon.Entries[i])) // If packet was successfull to send, remove it from list
      Beacon.Entries.erase(std::next(Beacon.Entries.begin() , i));
    else{
      break;
    }
  }

  for (size_t i = 0; i < Beacon.Exits.size();) { // Send notifications for exits
    if (httpService.sendExitPacket(Beacon.Exits[i])) // If packet was successfull to send, remove it from list
      Beacon.Exits.erase(std::next(Beacon.Exits.begin() , i));
    else {
      break;
    }
  }
}
