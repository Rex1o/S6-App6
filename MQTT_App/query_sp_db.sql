-- Création de la table des entrées et sorties
CREATE TABLE "entries" (
    "device_id" TEXT NOT NULL,
    "time" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "access_type" TEXT NOT NULL
);

-- Création de la table des utilisateurs
CREATE TABLE "persons" (
    "device_id" TEXT NOT NULL,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    PRIMARY KEY ("device_id")
);

-- Création de la table de statut vaccinal
CREATE TABLE "vaccination_status" (
    "email" TEXT NOT NULL,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "vaccination_status" TEXT NOT NULL
);

-- Création de la vue des entrées des appareils et des statuts vaccinaux des personnes
CREATE VIEW "device_vaccination_status" AS
SELECT 
    e.device_id, 
    e.time, 
    e.access_type, 
    p.first_name, 
    p.last_name, 
    vs.vaccination_status
FROM 
    entries e
JOIN 
    persons p ON e.device_id = p.device_id
JOIN
    vaccination_status vs ON p.email = vs.email;

-- Sélection de la vue d'association des données
select * from device_vaccination_status;

-- Insérer des données d'exemple dans la table des personnes
INSERT INTO persons (device_id, first_name, last_name, email) VALUES
('4a:1f:f8:90:b5:9d', 'David', 'Dupont', 'david.dupont@example.com');  -- iPhone

INSERT INTO vaccination_status (email, first_name, last_name, vaccination_status) VALUES
('david.dupont@example.com', 'David', 'Dupont', 'vacciné');

-- Mettre à jour l'ID de l'appareil pour David Dupont
UPDATE persons
SET device_id = '6a:4e:14:3b:4b:a7'
WHERE email = 'david.dupont@example.com';

-- Supprimer toutes les entrées de la table entries
DELETE FROM entries;