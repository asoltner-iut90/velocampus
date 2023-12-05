-- Suppression des tables si elles existent déjà
DROP TABLE IF EXISTS Possede, Contrat, Etudiant, Composante, Reparation, Velo, Etablissement, Formation, Type_velo, Piece;

-- Création de la table Piece
CREATE TABLE Piece(
   id_piece INT AUTO_INCREMENT,
   nom_piece VARCHAR(50),
   stock DOUBLE,
   PRIMARY KEY(id_piece)
);

-- Création de la table Type_velo
CREATE TABLE Type_velo(
   id_type_velo INT AUTO_INCREMENT,
   caution DECIMAL(15,2),
   nom_type_velo VARCHAR(50),
   num_serie VARCHAR(50),
   PRIMARY KEY(id_type_velo)
);

-- Création de la table Formation
CREATE TABLE Formation(
   id_formation INT AUTO_INCREMENT,
   nom_formation VARCHAR(50),
   PRIMARY KEY(id_formation)
);

-- Création de la table Etablissement
CREATE TABLE Etablissement(
   id_etablissement INT AUTO_INCREMENT,
   nom_etablissement VARCHAR(50),
   PRIMARY KEY(id_etablissement)
);

-- Création de la table Velo
CREATE TABLE Velo(
   id_velo INT AUTO_INCREMENT,
   id_type_velo INT NOT NULL,
   PRIMARY KEY(id_velo),
   FOREIGN KEY(id_type_velo) REFERENCES Type_velo(id_type_velo)
);

-- Création de la table Reparation
CREATE TABLE Reparation(
   id_reparation INT AUTO_INCREMENT,
   date_reparation DATE,
   descriptif TEXT,
   id_velo INT NOT NULL,
   PRIMARY KEY(id_reparation),
   FOREIGN KEY(id_velo) REFERENCES Velo(id_velo)
);

-- Création de la table Composante
CREATE TABLE Composante(
   id_composante INT AUTO_INCREMENT,
   id_formation INT NOT NULL,
   id_etablissement INT NOT NULL,
   PRIMARY KEY(id_composante),
   FOREIGN KEY(id_formation) REFERENCES Formation(id_formation),
   FOREIGN KEY(id_etablissement) REFERENCES Etablissement(id_etablissement)
);

-- Création de la table Etudiant
CREATE TABLE Etudiant(
   id_etudiant INT AUTO_INCREMENT,
   nom VARCHAR(50),
   prenom VARCHAR(50),
   email VARCHAR(50),
   telephone VARCHAR(10),
   id_composante INT NOT NULL,
   PRIMARY KEY(id_etudiant),
   FOREIGN KEY(id_composante) REFERENCES Composante(id_composante)
);

-- Création de la table Contrat
CREATE TABLE Contrat(
   id_contrat INT AUTO_INCREMENT,
   date_debut DATE,
   date_fin DATE,
   id_etudiant INT NOT NULL,
   id_velo INT NOT NULL,
   PRIMARY KEY(id_contrat),
   FOREIGN KEY(id_etudiant) REFERENCES Etudiant(id_etudiant),
   FOREIGN KEY(id_velo) REFERENCES Velo(id_velo)
);

-- Création de la table Possede
CREATE TABLE Possede(
   id_velo INT,
   id_piece INT,
   PRIMARY KEY(id_velo, id_piece),
   FOREIGN KEY(id_velo) REFERENCES Velo(id_velo),
   FOREIGN KEY(id_piece) REFERENCES Piece(id_piece)
);

-- Insertion dans la table Piece
INSERT INTO Piece (nom_piece, stock) VALUES
    ('Roue', 20),
    ('Pédale', 30),
    ('Guidon', 15),
    ('Selle', 0);

-- Insertion dans la table Type_velo
INSERT INTO Type_velo (caution, nom_type_velo, num_serie) VALUES
    (50.00, 'VTT', 'VT123'),
    (40.00, 'Vélo de route', 'VR456'),
    (60.00, 'Vélo électrique', 'VE789');

-- Insertion dans la table Formation
INSERT INTO Formation (nom_formation) VALUES
    ('Informatique'),
    ('GEII');

-- Insertion dans la table Etablissement
INSERT INTO Etablissement (nom_etablissement) VALUES
    ('IUT Nord Franche-Comte');

-- Insertion dans la table Velo
INSERT INTO Velo (id_type_velo) VALUES
    (1),
    (2),
    (3);

-- Insertion dans la table Reparation
INSERT INTO Reparation (date_reparation, descriptif, id_velo) VALUES
    ('2023-09-20', 'Réparation du frein', 2),
    ('2023-10-15', 'Changement de pneu', 1),
    ('2023-11-05', 'Entretien électrique', 3),
    ('2023-11-10', 'Changement de chaîne', 2),
    ('2023-11-15', 'Réparation de la selle', 2);

-- Insertion dans la table Composante
INSERT INTO Composante (id_formation, id_etablissement) VALUES
    (1, 1),
    (2, 1);


-- Insertion dans la table Etudiant
INSERT INTO Etudiant (nom, prenom, email, telephone, id_composante) VALUES
    ('Durand', 'Jean', 'durand.jean@edu.univ-fcomte.fr', '0678901456', 1),
    ('Dubois', 'Sophie', 'dubois.sophie@edu.univ-fcomte.fr', '0628003432', 1),
    ('Martin', 'Pierre', 'martin.pierre@edu.univ-fcomte.fr', '0751942154', 2);

-- Insertion dans la table Contrat
INSERT INTO Contrat (date_debut, date_fin, id_etudiant, id_velo) VALUES
    ('2023-10-01', '2023-11-01', 1, 1),
    ('2023-09-15', '2023-10-15', 2, 2),
    ('2023-11-01', '2023-12-01', 3, 3),
    ('2023-11-05', '2023-12-05', 1, 3),
    ('2023-10-20', '2023-11-20', 3, 1);

-- Insertion dans la table Possede
INSERT INTO Possede (id_velo, id_piece) VALUES
    (1, 1),
    (2, 2),
    (3, 3);
