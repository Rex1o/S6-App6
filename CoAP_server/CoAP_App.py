import aiocoap
import aiocoap.resource
import asyncio
import os
import sqlite3
import json

# Chemin vers la base de données assurance_db.db
db_path = os.getenv("DB_PATH", "/app/assurance_db.db")

# Écrire dans la table entries de la base de données
def write_to_db(table, device_id, time, status):
    """
    Écrire des données dans la base de données SQLite.
    """

    # Ouvrir une connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Insérer des données dans la table spécifiée
    query = f"INSERT INTO {table} (device_id, time, access_type) VALUES (?, ?, ?)"
    cursor.execute(query, (device_id, time, status))
    conn.commit()
    
    # Fermer la connexion
    conn.close()

# Classe pour gérer les requêtes CoAP liées aux entrées
class EntriesResource(aiocoap.resource.Resource):
    """
    Ressource pour gérer les requêtes CoAP liées aux entrées (POST).
    """
    
    async def render_post(self, request):
        """
        Gérer les requêtes POST pour créer des entrées.
        """
        try:
            print(f"📥 CoAP POST reçu: {request.payload}")

            # Récupérer le payload de la requête
            data = json.loads(request.payload.decode('utf-8'))
            device_id = data["device_id"]
            time = data["time"]
            status = data["status"]
            
            print(f"📝 Écriture dans la BD: device_id={device_id}, time={time}, status={status}")

            # Écrire dans la base de données
            write_to_db("entries", device_id, time, status)

            print("✅ Données écrites dans la base de données avec succès")

            return aiocoap.Message(code=aiocoap.Code.CREATED, payload=b"CoAP entre cree avec succes.")

        except Exception as e:
            print(f"❌ Erreur lors du traitement de la requête CoAP: {e}")
            return aiocoap.Message(code=aiocoap.Code.INTERNAL_SERVER_ERROR, payload=b"Erreur lors du traitement de la requete.")
        
async def coap_server():
    """
    Démarrer le serveur CoAP.
    """

    # Créer le site CoAP et ajouter la ressource pour les entrées
    root = aiocoap.resource.Site()
    root.add_resource(["entries"], EntriesResource())

    # Démarrer le serveur CoAP sur l'adresse 0.0.0.0:5683
    print("🚀 Démarrage du serveur CoAP sur 0.0.0.0:5683...")
    await aiocoap.Context.create_server_context(root, bind=('0.0.0.0', 5683))
    print("✅ Le serveur CoAP fonctionne sur le port 5683...")

    # Garder le serveur en fonctionnement
    await asyncio.get_event_loop().create_future()


if __name__ == "__main__":
    print("Démarrage du serveur CoAP...")
    asyncio.run(coap_server())