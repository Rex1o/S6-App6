#include <WiFi.h>
#include <PubSubClient.h>
#include "BLEBeaconNotifier.h"

// === Configuration Wi-Fi ===
const char* ssid = "EasyAmongUs_24";
const char* password = "RedPantsAmigo1";
// WiFiClient wifiClient;
BLEBeaconNotifier Beacon;

// === Connexion au Wi-Fi ===
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connexion à ");
  Serial.println(ssid);

  // WiFi.begin(ssid, password);

  // while (WiFi.status() != WL_CONNECTED) {
  //   delay(500);
  //   Serial.print(".");
  // }

  Serial.println("\nWiFi connecté");
  Serial.print("Adresse IP : ");
  Serial.println(WiFi.localIP());
}

// === Setup initial ===
void setup() {
  Serial.begin(115200);
  setup_wifi();
  Beacon.setup();
}

// === Boucle principale ===
void loop() {
  Beacon.loop();
}
