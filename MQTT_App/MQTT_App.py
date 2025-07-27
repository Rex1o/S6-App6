import paho.mqtt.client as mqtt
import sqlite3
import os
import json
import time

# Topic pour les entrées
topic = "device/entries"

# Récupérer les variables d'environnement
db_name = os.getenv("DB_NAME", "sante_publique_db.db")
db_path = os.getenv("DB_PATH", f"/app/{db_name}")

# Écrire dans la table entries de santé publique
def write_to_db(table, device_id, time, status):
    """
    Écrire une entrée dans la base de données de santé publique.
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

# Callback pour la connexion MQTT
def on_connect(client, userdata, flags, rc):
    """
    Callback pour la connexion au broker MQTT.
    """

    print("Connected with result code " + str(rc))
    
    # S'abonner au topic
    client.subscribe(topic, qos=2)

# Callback pour les messages reçus
def on_message(client, userdata, msg):
    """
    Callback pour les messages reçus sur le topic MQTT.
    """

    print(f"Message reçu sur le topic {msg.topic}: {msg.payload.decode()}")

    # Récupérer les données du message
    data = json.loads(msg.payload.decode())
    device_id = data.get("device_id")
    time = data.get("time")
    status = data.get("status")
    
    # Enregistrer les données dans la base de données de santé publique
    write_to_db("entries", device_id, time, status)


def main():
    
    # Configurer le client MQTT
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    # Se connecter au broker Mosquitto
    while True:
        try:
            mqtt_client.connect("broker", port=1883, keepalive=60)
            break
        except Exception as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)
    
    # Boucle principale pour recevoir les messages
    mqtt_client.loop_forever()

if __name__ == "__main__":
    main()