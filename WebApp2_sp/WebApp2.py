import streamlit as st
import pandas as pd
import sqlite3
import os
import requests

def main():
    db_path = os.getenv("DB_PATH", "/app/sante_publique_db.db")

    # Vérifier si le fichier de base de données existe
    if not os.path.exists(db_path):
        st.error(f"Database file not found at {db_path}. Please check the DB_PATH environment variable.")
        return
    
    # Connexion à la base de données SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Sélectionner les données de la table
    query = """
    SELECT * FROM device_vaccination_status ORDER BY time DESC
    """
    cursor.execute(query)
    data = cursor.fetchall()

    # Récupérer les noms des colonnes
    cursor.execute("PRAGMA table_info(device_vaccination_status)")
    column_info = cursor.fetchall()
    column_names = [col[1] for col in column_info]

    # Convertir les données en DataFrame
    df = pd.DataFrame(data, columns=column_names)

    # Afficher le DataFrame
    st.title("Données d'entrée-sortie de la base de données santé publique")
    st.write(df)

    # Fermer la connexion
    conn.close()

if __name__ == "__main__":
    main()