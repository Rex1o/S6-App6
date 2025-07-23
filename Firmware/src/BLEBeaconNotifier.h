
#pragma once
#include <string>
#include <BLEScan.h>
#include <vector>

struct DeviceRequest
{
    float distance;
    BLEAddress address;
};


class BLEBeaconNotifier
{
private: // Consts
const std::string DEVICE_NAME = "Cool Team Beacon";
const uint8_t BEACON_UUID_BYTE_ARRAY[16] = {0x25,0xe5,0xc0,0xb8,0x4f,0xf8,0x4e,0x1b,0x9c,0x2e,0xbd,0x67,0x1e,0x9c,0x0f,0x90}; 
const std::string BEACON_UUID_STRING =  "25e5c0b8-4ff8-4e1b-9c2e-bd671e9c0f90";
const double MINIMUM_DISTANCE =  5; // Minimum distance between the device and beacon to be considered in the room in meters

private: // BLE services
// List of current devices
    std::vector<BLEAddress> _currentDevices;
    std::vector<DeviceRequest> _newScanDevices;
    void verifyConnectionState();
    BLEScan* _BLEScan;
public:
    inline BLEBeaconNotifier() {};
    inline ~BLEBeaconNotifier(){};
    void loop();
    void setup();
    bool isMatchingUUID(const uint8_t* payload, size_t len);
    float estimateDistance(int txPower, int rssi);
};