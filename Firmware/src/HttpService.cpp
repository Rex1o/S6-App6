#include "HttpService.h"
#include <HTTPClient.h>
#include <BLEAddress.h>
#include <sstream>

const uint8_t     HttpService::LED_GPIO = GPIO_NUM_2;
const std::string HttpService::SERVER_IP =  "192.168.0.62:5000";
std::string HttpService::POST_EXIT_API_ROUTE =  "http://" + SERVER_IP + "/exit";
std::string HttpService::POST_ENTRY_API_ROUTE =  "http://" + SERVER_IP + "/enter";
const std::string HttpService::ROOM_ID = "4";
WebServer HttpService::_server(80);


HttpService::HttpService (WiFiClient& wifiClient) : _wifiClient(wifiClient) {
}

void HttpService::setup() {
    pinMode(LED_GPIO, OUTPUT);
    _server.on("/on", handleOn);
    _server.on("/off", handleOff);
    _server.begin();
    Serial.println("HTTP server started");
}

void HttpService::loop(){
    _server.handleClient();
}

bool HttpService::sendExitPacket(Entry& entry){
    HTTPClient http;
    http.begin(_wifiClient, POST_EXIT_API_ROUTE.c_str());
    http.addHeader("Content-Type", "application/json");
    std::string message = entryToJson(entry);

    Serial.print("Sending exit packet: ");
    Serial.println(message.c_str());
    int httpResponseCode = http.POST(message.c_str());

    if (httpResponseCode != 200 && httpResponseCode != 201 && httpResponseCode != 202)    {
        Serial.println("Failed to send Exit packet");
        return false;
    }

    return true;
}

bool HttpService::sendEnterPacket(Entry& entry){
    HTTPClient http;
    http.begin(_wifiClient, POST_ENTRY_API_ROUTE.c_str());
    http.addHeader("Content-Type", "application/json");
    std::string message = entryToJson(entry);
    Serial.print("Sending Enter packet: ");
    Serial.println(message.c_str());
    int httpResponseCode = http.POST(message.c_str());
    if (httpResponseCode != 200 && httpResponseCode != 201 && httpResponseCode != 202)
    {
        Serial.println("Failed to send Enter packet");
        return false;
    }

    return true;
}

std::string HttpService::entryToJson(Entry& data) {
    std::ostringstream oss;
    oss << "{";
    
    oss << "\"room_id\": \""; 
    oss << ROOM_ID;
    oss << "\",";

    oss << "\"device_id\": \"";
    oss << data.address.toString();
    oss << "\",";

    oss << "\"time\": \"";
    char time_string[80]; // Buffer to store the formatted string
    strftime(time_string, sizeof(time_string), "%Y-%m-%d %H:%M:%S", &data.timeinfo);
    oss << time_string;
    oss << "\"";

    oss << "}";

    return oss.str();
}

void HttpService::handleOn() {
    Serial.println("Admin ON signal received");
    digitalWrite(LED_GPIO, HIGH);
    _server.send(200, "text/plain", "Success turned on");
}

void HttpService::handleOff() {
    Serial.println("Admin OFF signal received");
    digitalWrite(LED_GPIO, LOW);
    _server.send(200, "text/plain", "Success turned off");
}
