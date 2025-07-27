-- Création de la table des entrées et sorties
CREATE TABLE "entries" (
    "device_id" TEXT NOT NULL,
    "time" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "access_type" TEXT NOT NULL
);

-- Création de la table des personnes
CREATE TABLE "persons" (
    "device_id" TEXT NOT NULL,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    PRIMARY KEY ("device_id")
);

-- Création de la table d'information client
CREATE TABLE "client_info" (
    "email" TEXT NOT NULL,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "phone" TEXT NOT NULL,
    PRIMARY KEY ("email")
);

-- Création de la vue des entrées des appareils et des informations client
CREATE VIEW "device_client_info" AS
SELECT 
    e.device_id, 
    e.time, 
    e.access_type, 
    p.first_name, 
    p.last_name, 
    ci.phone
FROM 
    entries e
JOIN 
    persons p ON e.device_id = p.device_id
JOIN
    client_info ci ON p.email = ci.email;

-- Sélection de la vue d'association des données
SELECT * FROM device_client_info;

-- Supprimer toutes les entrées de la table entries
DELETE FROM entries;