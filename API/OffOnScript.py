import requests
import os

deviceIP = os.getenv("DEVICE_IP")


def TurnOn():
    response = requests.get("http://" + deviceIP + ":80/on")

def TurnOff():
    response = requests.get("http://" + deviceIP + ":80/off")

def main():
    TurnOn()


if __name__ == "__main__":
    main()
