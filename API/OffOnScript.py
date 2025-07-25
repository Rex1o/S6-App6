import requests
devicveIP = "192.168.0.24"


def TurnOn():
    response = requests.get("http://" + devicveIP + ":80/on")

def TurnOff():
    response = requests.get("http://" + devicveIP + ":80/off")

def main():
    TurnOn()


if __name__ == "__main__":
    main()
