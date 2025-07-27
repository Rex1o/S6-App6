import asyncio
from flask import Flask, jsonify, request
from OffOnScript import TurnOn, TurnOff
import os
import sqlite3
import paho.mqtt.client as mqtt
import json
import socket
import threading
import aiocoap

app = Flask(__name__)

# Récupérer les variables d'environnement
db_name = os.getenv("DB_NAME", "main_db.db")
db_path = os.getenv("DB_PATH", f"/app/{db_name}")

# Définition du topic
topic1 = "device/entries"



# Écrire dans la table entries locale
def write_to_db(table, device_id, time, status):
    """
    Écrire une entrée dans la base de données locale.
    """

    # Ouvrir une connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insérer les données dans la table
    query = f"INSERT INTO {table} (device_id, time, access_type) VALUES (?, ?, ?)"
    cursor.execute(query, (device_id, time, status))
    conn.commit()

    # Fermer la connexion
    conn.close()

# Publier au topic MQTT
def publish_mqtt(device_id, timestamp, status, topic):
    """
    Fonction MQTT qui s'exécute dans un thread séparé
    """

    try:
        IP_ADDRESS = socket.gethostbyname("broker")
        print(f"🌐 MQTT broker IP: {IP_ADDRESS}")
        
        # Créer un client MQTT
        mqtt_client = mqtt.Client()
        mqtt_client.connect(IP_ADDRESS, port=1883, keepalive=60)
        
        # Récupérer le payload
        payload = json.dumps({
            "device_id": device_id,
            "time": timestamp,
            "status": status
        })
        
        # Publier le message
        print(f"📤 Publishing to {topic}: {payload}")
        result = mqtt_client.publish(topic, payload, qos=1)
        mqtt_client.disconnect()
        print("✅ MQTT message published successfully (background)")
        
    except Exception as e:
        print(f"❌ MQTT background publish failed: {e}")


# Fonction CoAP pour notifier le serveur CoAP
async def _coap_post(device_id, timestamp, status):
    """
    Fonction CoAP qui s'exécute dans un thread séparé
    """

    try:
        # Créer un contexte CoAP et envoyer une requête POST
        context = await aiocoap.Context.create_client_context()
        
        # Préparer le payload
        payload = json.dumps({
            "device_id": device_id,
            "time": timestamp,
            "status": status
        }).encode('utf-8')

        # Créer la requête POST
        request = aiocoap.Message(
            code=aiocoap.Code.POST,
            uri='coap://coap_server:5683/entries',
            payload=payload
        )

        # Envoyer la requête et attendre la réponse
        response = await context.request(request).response
        print(f"✅ CoAP POST successful: {response.code} {response.payload.decode('utf-8')}")
        
        # Retourner le code et le payload de la réponse
        return response.code, response.payload.decode('utf-8')
        
    except Exception as e:
        print(f"❌ CoAP POST failed: {e}")

# Notifier le serveur CoAP en arrière-plan
def notify_coap(device_id, timestamp, status):
    """
    Notifie le serveur CoAP en arrière-plan
    """

    # Préparer le payload pour CoAP
    payload = {
        "device_id": device_id,
        "time": timestamp,
        "status": status
    }

    try:
        # Exécuter la fonction CoAP dans un thread séparé
        response = asyncio.run(_coap_post(device_id, timestamp, status))
        print(f"CoAP response: {response}")
    except Exception as e:
        print(f"❌ CoAP notification failed: {e}")


# POST reçu du ESP32 lors d'une sortie
@app.route('/exit', methods=['POST'])
def add_exit():
    """
    Fonction pour traiter les requêtes POST de sortie du ESP32.
    """

    # Récupérer le JSON de l'information reçue
    new_item = request.json
    print(f"Nouvelle sortie reçue: {new_item}")

    # Écrire la sortie dans la base de données locale
    write_to_db("entries", new_item['device_id'], new_item['time'], "sortie")

    # Publier au topic MQTT sur un autre thread pour ne pas bloquer le serveur et avoir une récursion infinie
    print("📤 Publishing to MQTT (from ESP32)")
    thread = threading.Thread(target=publish_mqtt, args=(new_item['device_id'], new_item['time'], "sortie", topic1))
    thread.daemon = True
    thread.start()
    print("🚀 MQTT publish started in background")

    # Notifier le serveur CoAP en arrière-plan
    notify_coap(new_item['device_id'], new_item['time'], "sortie")

    # Retourner la réponse
    return jsonify(new_item), 201

# POST reçu du ESP32 lors d'une entrée
@app.route('/enter', methods=['POST'])
def add_entry():
    """
    Fonction pour traiter les requêtes POST d'entrée du ESP32.
    """

    # Récupérer le JSON de l'information reçue
    new_item = request.json
    print(f"Nouvelle entrée reçue: {new_item}")

    # Écrire l'entrée dans la base de données locale
    write_to_db("entries", new_item['device_id'], new_item['time'], "entre")

    # Publier au topic MQTT sur un autre thread pour ne pas bloquer le serveur et avoir une récursion infinie
    print("📤 Publishing to MQTT (from ESP32)")
    thread = threading.Thread(target=publish_mqtt, args=(new_item['device_id'], new_item['time'], "entre", topic1))
    thread.daemon = True
    thread.start()
    print("🚀 MQTT publish started in background")

    # Notifier le serveur CoAP en arrière-plan
    notify_coap(new_item['device_id'], new_item['time'], "entre")

    print("✅ Entry processed successfully!")
    
    # Retourner la réponse
    return jsonify(new_item), 201

# GET, pour allumer la DEL
@app.route('/on', methods=['GET'])
def get_on():
    """
    Fonction pour allumer la DEL.
    """
    
    TurnOn()
    return jsonify({"status": "on"}), 200

# GET, pour éteindre la DEL
@app.route('/off', methods=['GET'])
def get_off():
    """
    Fonction pour éteindre la DEL.
    """

    TurnOff()
    return jsonify({"status": "off"}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
