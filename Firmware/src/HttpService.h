#pragma once
#include <WebServer.h>
#include "BLEBeaconNotifier.h"

class HttpService
{
public:
    static const uint8_t LED_GPIO;
    static const char* SSID;
    static const char* PASSWORD;
    static const IPAddress local_IP;
    static const IPAddress gateway;
    static const IPAddress subnet;
    static const std::string SERVER_IP;
    static std::string POST_EXIT_API_ROUTE;
    static std::string POST_ENTRY_API_ROUTE;
    static const std::string ROOM_ID;

    HttpService(WiFiClient& wifiClient);
    inline ~HttpService() {};
    void setup();
    void loop();

    // returns true if packet is sucessfully sent
    bool sendExitPacket(Entry& entry);
    // returns true if packet is sucessfully sent
    bool sendEnterPacket(Entry& entry);

    private:
    static void handleOn();
    static void handleOff();
    WiFiClient& _wifiClient;
    static WebServer _server;

    std::string entryToJson(Entry& data);
};
