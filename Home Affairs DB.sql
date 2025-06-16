
-- Citizen Table
CREATE TABLE IF NOT EXISTS citizen (
    idNumber VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    dateOfBirth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    nationality VARCHAR(100),
    homeLanguage VARCHAR(100)
);

-- Address Table
CREATE TABLE IF NOT EXISTS address (
    addressId INT AUTO_INCREMENT PRIMARY KEY,
    idNumber VARCHAR(20) NOT NULL,
    streetAddress VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    province VARCHAR(100) NOT NULL,
    postalCode VARCHAR(10) NOT NULL,
    FOREIGN KEY (idNumber) REFERENCES citizen(idNumber)
);

-- Document Table
CREATE TABLE IF NOT EXISTS document (
    documentId INT AUTO_INCREMENT PRIMARY KEY,
    idNumber VARCHAR(20) NOT NULL,
    documentType VARCHAR(100) NOT NULL,
    issueDate DATE NOT NULL,
    expiryDate DATE,
    documentStatus VARCHAR(50) NOT NULL,
    FOREIGN KEY (idNumber) REFERENCES citizen(idNumber)
);

-- BirthCertificate Table
CREATE TABLE IF NOT EXISTS birthcertificate (
    birthCertId INT AUTO_INCREMENT PRIMARY KEY,
    idNumber VARCHAR(20) NOT NULL,
    placeOfBirth VARCHAR(100) NOT NULL,
    birthDate DATE NOT NULL,
    registeredBy VARCHAR(100) NOT NULL,
    registrationDate DATE NOT NULL,
    FOREIGN KEY (idNumber) REFERENCES citizen(idNumber)
);

-- DeathCertificate Table
CREATE TABLE IF NOT EXISTS deathcertificate (
    deathCertId INT AUTO_INCREMENT PRIMARY KEY,
    idNumber VARCHAR(20) NOT NULL,
    deathDate DATE NOT NULL,
    causeOfDeath VARCHAR(255) NOT NULL,
    placeOfDeath VARCHAR(100) NOT NULL,
    FOREIGN KEY (idNumber) REFERENCES citizen(idNumber)
);

-- Passport Table
CREATE TABLE IF NOT EXISTS passport (
    passportId INT AUTO_INCREMENT PRIMARY KEY,
    idNumber VARCHAR(20) NOT NULL,
    issueDate DATE NOT NULL,
    expiryDate DATE NOT NULL,
    countryOfIssue VARCHAR(100) NOT NULL,
    FOREIGN KEY (idNumber) REFERENCES citizen(idNumber)
);

-- Photo Table
CREATE TABLE IF NOT EXISTS photo (
    photoId INT AUTO_INCREMENT PRIMARY KEY,
    idNumber VARCHAR(20) NOT NULL,
    uploadDate DATE NOT NULL,
    FOREIGN KEY (idNumber) REFERENCES citizen(idNumber)
);

-- Marriage Table
CREATE TABLE IF NOT EXISTS marriage (
    marriageId INT AUTO_INCREMENT PRIMARY KEY,
    marriageDate DATE NOT NULL,
    marriageStatus VARCHAR(50) NOT NULL,
    marriageType VARCHAR(50) NOT NULL
);

-- MarriageParticipant Table
CREATE TABLE IF NOT EXISTS marriageparticipant (
    participantId INT AUTO_INCREMENT PRIMARY KEY,
    marriageId INT NOT NULL,
    citizenId VARCHAR(20) NOT NULL,
    role VARCHAR(50) NOT NULL,
    marriageType VARCHAR(50) NOT NULL,
    FOREIGN KEY (marriageId) REFERENCES marriage(marriageId),
    FOREIGN KEY (citizenId) REFERENCES citizen(idNumber)
);

-- Insert Sample Data
INSERT INTO citizen (idNumber, name, surname, dateOfBirth, gender, nationality, homeLanguage) VALUES
('8001015009087', 'John', 'Doe', '1980-01-01', 'Male', 'South African', 'English'),
('9002024800082', 'Jane', 'Smith', '1990-02-02', 'Female', 'South African', 'Afrikaans'),
('7503035500075', 'Alice', 'Johnson', '1975-03-03', 'Female', 'South African', 'Zulu'),
('8904044400089', 'Bob', 'Brown', '1989-04-04', 'Male', 'South African', 'Xhosa'),
('9505053300095', 'Eve', 'Williams', '1995-05-05', 'Female', 'South African', 'Sotho');

INSERT INTO address (idNumber, streetAddress, city, province, postalCode) VALUES
('8001015009087', '123 Main St', 'Johannesburg', 'Gauteng', '2000'),
('9002024800082', '456 Oak Ave', 'Cape Town', 'Western Cape', '8001'),
('7503035500075', '789 Pine Rd', 'Durban', 'KwaZulu-Natal', '4000'),
('8904044400089', '321 Elm Blvd', 'Pretoria', 'Gauteng', '0002'),
('9505053300095', '654 Maple Ln', 'Bloemfontein', 'Free State', '9301');

INSERT INTO document (idNumber, documentType, issueDate, expiryDate, documentStatus) VALUES
('8001015009087', 'ID Card', '2010-01-01', '2030-01-01', 'Active'),
('9002024800082', 'ID Card', '2015-05-15', '2035-05-15', 'Active'),
('7503035500075', 'ID Card', '2005-03-10', '2025-03-10', 'Expired'),
('8904044400089', 'Drivers License', '2020-02-20', '2030-02-20', 'Active'),
('9505053300095', 'Passport', '2022-12-01', '2032-12-01', 'Active');

INSERT INTO birthcertificate (idNumber, placeOfBirth, birthDate, registeredBy, registrationDate) VALUES
('8001015009087', 'Johannesburg Hospital', '1980-01-01', 'Dr. Smith', '1980-01-05'),
('9002024800082', 'Cape Town Maternity', '1990-02-02', 'Nurse Johnson', '1990-02-07'),
('7503035500075', 'Durban Clinic', '1975-03-03', 'Midwife Brown', '1975-03-10'),
('8904044400089', 'Pretoria Hospital', '1989-04-04', 'Dr. Wilson', '1989-04-09'),
('9505053300095', 'Bloemfontein Clinic', '1995-05-05', 'Nurse Davis', '1995-05-10');

INSERT INTO passport (idNumber, issueDate, expiryDate, countryOfIssue) VALUES
('8001015009087', '2020-01-01', '2030-01-01', 'South Africa'),
('9002024800082', '2021-03-15', '2031-03-15', 'South Africa'),
('7503035500075', '2018-06-01', '2028-06-01', 'South Africa'),
('8904044400089', '2022-05-20', '2032-05-20', 'South Africa'),
('9505053300095', '2023-01-10', '2033-01-10', 'South Africa');

INSERT INTO marriage (marriageDate, marriageStatus, marriageType) VALUES
('2005-06-15', 'Married', 'Civil'),
('2010-09-20', 'Divorced', 'Traditional'),
('2018-03-12', 'Married', 'Religious');

INSERT INTO marriageparticipant (marriageId, citizenId, role, marriageType) VALUES
(1, '8001015009087', 'Bridegroom', 'Civil'),
(1, '9002024800082', 'Bride', 'Civil'),
(2, '7503035500075', 'Bridegroom', 'Traditional'),
(2, '8904044400089', 'Bride', 'Traditional'),
(3, '9505053300095', 'Bride', 'Religious');

-- Add sample photos (empty BLOB for demonstration)
INSERT INTO photo (idNumber, uploadDate) VALUES
('8001015009087', '2023-01-01'),
('9002024800082', '2023-02-15'),
('7503035500075', '2023-03-20'),
('8904044400089', '2023-04-25'),
('9505053300095', '2023-05-30');