-- Création de la table des entrées et sorties
CREATE TABLE "entries" (
    "device_id" TEXT NOT NULL,
    "time" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "access_type" TEXT NOT NULL
);

-- Sélection de toutes les entrées
SELECT * FROM "entries";