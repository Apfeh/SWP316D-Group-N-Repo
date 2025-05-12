-- Citizen table
CREATE TABLE Citizen (
    idNumber VARCHAR(20) PRIMARY KEY,
    name VARCHAR(50),
    surname VARCHAR(50),
    dateOfBirth DATE,
    gender VARCHAR(10),
    nationality VARCHAR(50),
    homeLanguage VARCHAR(50)
);

-- Address table
CREATE TABLE Address (
    addressId INT PRIMARY KEY AUTO_INCREMENT,
    idNumber VARCHAR(20),
    streetAddress VARCHAR(100),
    city VARCHAR(50),
    province VARCHAR(50),
    postalCode VARCHAR(10),
    FOREIGN KEY (idNumber) REFERENCES Citizen(idNumber)
);

-- Document table
CREATE TABLE Document (
    documentId INT PRIMARY KEY AUTO_INCREMENT,
    idNumber VARCHAR(20),
    documentType VARCHAR(50),
    issueDate DATE,
    expiryDate DATE,
    documentStatus VARCHAR(20),
    FOREIGN KEY (idNumber) REFERENCES Citizen(idNumber)
);

-- BirthCertificate table
CREATE TABLE BirthCertificate (
    birthCertId INT PRIMARY KEY AUTO_INCREMENT,
    idNumber VARCHAR(20),
    placeOfBirth VARCHAR(100),
    birthDate DATE,
    registeredBy VARCHAR(50),
    registrationDate DATE,
    FOREIGN KEY (idNumber) REFERENCES Citizen(idNumber)
);

-- DeathCertificate table
CREATE TABLE DeathCertificate (
    deathCertId INT PRIMARY KEY AUTO_INCREMENT,
    idNumber VARCHAR(20),
    deathDate DATE,
    causeOfDeath VARCHAR(100),
    placeOfDeath VARCHAR(100),
    FOREIGN KEY (idNumber) REFERENCES Citizen(idNumber)
);

-- Passport table
CREATE TABLE Passport (
    passportId INT PRIMARY KEY AUTO_INCREMENT,
    idNumber VARCHAR(20),
    issueDate DATE,
    expiryDate DATE,
    countryOfIssue VARCHAR(50),
    FOREIGN KEY (idNumber) REFERENCES Citizen(idNumber)
);

-- Photo table
CREATE TABLE Photo (
    photoId INT PRIMARY KEY AUTO_INCREMENT,
    idNumber VARCHAR(20),
    imagePath VARCHAR(255),
    uploadDate DATE,
    FOREIGN KEY (idNumber) REFERENCES Citizen(idNumber)
);

-- Marriage table
CREATE TABLE Marriage (
    marriageId INT PRIMARY KEY AUTO_INCREMENT,
    marriageDate DATE,
    marriageStatus VARCHAR(20),
    marriageType VARCHAR(50)
);

-- MarriageParticipant table
CREATE TABLE MarriageParticipant (
    participantId INT PRIMARY KEY AUTO_INCREMENT,
    marriageId INT,
    citizenId VARCHAR(20),
    role VARCHAR(20),
    marriageType VARCHAR(50),
    FOREIGN KEY (marriageId) REFERENCES Marriage(marriageId),
    FOREIGN KEY (citizenId) REFERENCES Citizen(idNumber)
);