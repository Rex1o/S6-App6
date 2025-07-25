#include "BLEBeaconNotifier.h"
#include <Arduino.h>
#include <vector>
#include <BLEDevice.h>
#include <unordered_set>

void printHexPayload(const uint8_t* payload, int len) {
  Serial.print("Payload (hex): ");
  for (int i = 0; i < len; i++) {
    if (payload[i] < 16) Serial.print("0");
    Serial.print(payload[i], HEX);
    Serial.print(" ");
  }
  Serial.println();
}

void BLEBeaconNotifier::setup()
{
  Serial.println("Beacon Init");
  BLEDevice::init(DEVICE_NAME);
  _BLEScan = BLEDevice::getScan();
  _BLEScan->setActiveScan(true);
  _BLEScan->setInterval(100);
  _BLEScan->setWindow(99);
}

void BLEBeaconNotifier::verifyConnectionState()
{
  tm timeinfo;
  if (!getLocalTime(&timeinfo))
  {
    
  }

  // Filter by size
  for (size_t i = 0; i < _newScanDevices.size();)
  {
    DeviceRequest request = _newScanDevices[i];
    if (request.distance > MINIMUM_DISTANCE)
    {
      _newScanDevices.erase(std::next(_newScanDevices.begin() , i));
    }
    else
    {
      ++i;
    }
  }

  // Remove all devices in current device that are not in newscan
  for (size_t i = 0; i < _currentDevices.size();)
  {
    bool deviceFound = false;
    BLEAddress address = _currentDevices[i];
    for (size_t j = 0; j < _newScanDevices.size();)
    {
      DeviceRequest request = _newScanDevices[j];
      if (request.address.equals(address)) { // Device is still good and can be kept 
        Serial.print("Device already in the room: ");
        Serial.println(address.toString().c_str());
        deviceFound = true;
        _newScanDevices.erase(std::next(_newScanDevices.begin() , j)); // Device already exists, get rid of it in this list
        break;
      }
      else {
         j++;
      }
    }

    if (!deviceFound) { // If no devices matched in both lists, device needs to be removed
      Serial.print("Left the room: ");
      Serial.println(address.toString().c_str());
      Exits.push_back(Entry{timeinfo, address});
      _currentDevices.erase(_currentDevices.begin() + i);
    } else {
      ++i;
    }
  }

  // Add all devices in new scans that were not in current deive
  for (size_t i = 0; i < _newScanDevices.size(); i++) {
    DeviceRequest request = _newScanDevices[i];
    Entries.push_back(Entry{timeinfo, request.address});
    _currentDevices.push_back(request.address);
    Serial.print("Entered the room: ");
    Serial.println(request.address.toString().c_str());
  }
  _newScanDevices.clear(); // Clear the newScanDevices vector
}

void BLEBeaconNotifier::loop() {
    BLEScanResults results = _BLEScan->start(3, false);

    for (int i = 0; i < results.getCount(); i++) {
        BLEAdvertisedDevice dev = results.getDevice(i);
        std::string data = dev.getManufacturerData();
        const uint8_t *payload = (const uint8_t *)data.data();
        int len = data.length();

        if (!isMatchingUUID(payload, len)) // If the UUID is incorrect
            continue;

        int RSSI = (~(int8_t)payload[24] + 1) * -1; // RSSI

        int txPower = dev.getTXPower();      // RSSI calculated from the bluetooth module

        int RSSILib = dev.getRSSI();

        float distance = estimateDistance(txPower, RSSI);

        BLEAddress address = dev.getAddress();
        _newScanDevices.push_back(DeviceRequest{distance, address});
    }
    verifyConnectionState();
    _BLEScan->clearResults();
    delay(500);
}

bool BLEBeaconNotifier::isMatchingUUID(const uint8_t* payload, size_t len) {
  if (len < 25)
    return false; 

  if (payload[0] != 0x4C || payload[1] != 0x00 || payload[2] != 0x02 || payload[3] != 0x15)
    return false;

  for (int i = 0; i < 16; ++i) {
    if (payload[4 + i] != BEACON_UUID_BYTE_ARRAY[i])
      return false;
  }

  return true;
}

// https://vocal.media/01/convert-rssi-value-of-the-ble-bluetooth-low-energy-beacons-to-meters
float BLEBeaconNotifier::estimateDistance(int txPower, int rssi) {
  return pow(10.0,((double)txPower - (double)rssi) / 100.0);
}