import streamlit
import pandas as pd
import sqlite3
import os
import requests
import logging


def main():
    db_path = os.getenv("DB_PATH", "/app/main_db.db")

    # Vérifier si le fichier de base de données existe
    if not os.path.exists(db_path):
        streamlit.error(f"Database file not found at {db_path}. Please check the DB_PATH environment variable.")
        return
    
    # Connexion à la base de données SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Sélectionner les données de la table
    query = """
    SELECT * FROM entries ORDER BY time DESC
    """
    cursor.execute(query)
    data = cursor.fetchall()

    # Récupérer les noms des colonnes
    cursor.execute("PRAGMA table_info(entries)")
    column_info = cursor.fetchall()
    column_names = [col[1] for col in column_info]
    
    # Convertir les données en DataFrame
    df = pd.DataFrame(data, columns=column_names)

    # Afficher les données dans Streamlit
    streamlit.title("Données d'entrée-sortie de la base de données locale")

    # Afficher une checkbox pour allumer et éteindre la DEL
    if streamlit.checkbox("Allumer la DEL"):
        try:
            # Appel à l'API pour allumer la DEL. control est accessible via le service du docker-compose
            response = requests.get("http://control.:5000/on")
            if response.status_code == 200:
                streamlit.success("DEL allumée.")
            else:
                streamlit.error("Erreur lors de l'allumage de la DEL.")
        except requests.RequestException as e:
            streamlit.error(f"Erreur de connexion à l'API : {e}")
    else:
        try:
            # Appel à l'API pour éteindre la DEL. control est accessible via le service du docker-compose
            response = requests.get("http://control.:5000/off")
            if response.status_code == 200:
                streamlit.error("DEL éteinte.")
            else:
                streamlit.error("Erreur lors de l'extinction de la DEL.")
        except requests.RequestException as e:
            streamlit.error(f"Erreur de connexion à l'API : {e}")

    # Afficher le DataFrame
    streamlit.write(df)

    # Fermer la connexion à la base de données
    conn.close()


if __name__ == "__main__":
    main()