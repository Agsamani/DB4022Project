CREATE TABLE State (
  StateID INT PRIMARY KEY,
  SName VARCHAR(255) NOT NULL
);

CREATE TABLE City (
  CityID INT PRIMARY KEY,
  CName VARCHAR(255) NOT NULL,
  StateID INT NOT NULL,
  FOREIGN KEY(StateID) REFERENCES State(StateID)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Administrator (
  AdminID INT PRIMARY KEY,
  FirstName VARCHAR(255) NOT NULL,
  LastName VARCHAR(255) NOT NULL,
  Email VARCHAR(255),
  Phone VARCHAR(11)
);

CREATE TABLE Publisher (
  PubID INT PRIMARY KEY,
  IsActive BOOLEAN DEFAULT TRUE NOT NULL,
  RegDate TIMESTAMP NOT NULL
);

CREATE TABLE NormalUser (
  PubID INT,
  FirstName VARCHAR(255) NOT NULL,
  LastName VARCHAR(255) NOT NULL,
  Email VARCHAR(255),
  Phone VARCHAR(11),
  CityID INT NOT NULL,
  FOREIGN KEY(CityID) REFERENCES City(CityID),
  PRIMARY KEY(PubID),
  FOREIGN KEY(PubID) REFERENCES Publisher(PubID)
    ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE BusinessCategory (
  CatID INT PRIMARY KEY,
  CatName VARCHAR(255) NOT NULL
);

CREATE TABLE Business (
  PubID INT,
  BName VARCHAR(255) NOT NULL,
  CatID INT,
  RegistrationNum BIGINT NOT NULL,
  CityID INT NOT NULL,
  FOREIGN KEY(CityID) REFERENCES City(CityID),
  PRIMARY KEY(PubID),
  FOREIGN KEY(PubID) REFERENCES Publisher(PubID)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(CatID) REFERENCES BusinessCategory(CatID)
);


CREATE TABLE AdCategory (
  CatID INT PRIMARY KEY,
  CatName VARCHAR(255) NOT NULL
);

CREATE TABLE Advertisement (
  AdvertisementID INT,
  PubID INT NOT NULL,
  Title VARCHAR(255) NOT NULL,
  Price INT,
  CreationDate TIMESTAMP NOT NULL,
  CityID INT NOT NULL,
  UpdateDate TIMESTAMP,
  AdDesc VARCHAR(511),
  CatID INT NOT NULL DEFAULT 0,
  PRIMARY KEY(AdvertisementID),
  FOREIGN KEY(PubID) REFERENCES Publisher(PubID)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(CityID) REFERENCES City(CityID),
  FOREIGN KEY(CatID) REFERENCES AdCategory(CatID)
);


CREATE TABLE StatusState (
  AdStateID INT PRIMARY KEY,
  AdStateName VARCHAR(255) NOT NULL
);

CREATE TABLE AdStatus (
  AdvertisementID INT,
  AdStateID INT NOT NULL DEFAULT 0,
  AdminComment VARCHAR(255),
  UpdatedAt TIMESTAMP,
  PRIMARY KEY(AdvertisementID),
  FOREIGN KEY(AdvertisementID) REFERENCES Advertisement(AdvertisementID)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(AdStateID) REFERENCES StatusState(AdStateID)
);


CREATE TABLE ReportCategory (
  CatID INT PRIMARY KEY,
  CatName VARCHAR(255) NOT NULL
);

CREATE TABLE Report (
  AdvertisementID INT,
  ReportID INT,
  UserID INT NOT NULL,
  CatID INT,
  RDesc VARCHAR(511),
  PRIMARY KEY(AdvertisementID, ReportID),
  FOREIGN KEY(AdvertisementID) REFERENCES Advertisement(AdvertisementID)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(UserID) REFERENCES NormalUser(PubID)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(CatID) REFERENCES ReportCategory(CatID)
);

CREATE TABLE HomeAppliance (
  AdvertisementID INT,
  Brand VARCHAR(255),
  Material VARCHAR(255),
  PRIMARY KEY(AdvertisementID),
  FOREIGN KEY(AdvertisementID) REFERENCES Advertisement(AdvertisementID)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Vehicle (
  AdvertisementID INT,
  Brand VARCHAR(255),
  ProductionYear INT,
  PRIMARY KEY(AdvertisementID),
  FOREIGN KEY(AdvertisementID) REFERENCES Advertisement(AdvertisementID)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE RealEstate (
  AdvertisementID INT,
  Area INT,
  ConstructionDate DATE,
  PRIMARY KEY(AdvertisementID),
  FOREIGN KEY(AdvertisementID) REFERENCES Advertisement(AdvertisementID)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE DigitalProduct (
  AdvertisementID INT,
  Brand VARCHAR(255),
  Model VARCHAR(255),
  PRIMARY KEY(AdvertisementID),
  FOREIGN KEY(AdvertisementID) REFERENCES Advertisement(AdvertisementID)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Other (
  AdvertisementID INT,
  PRIMARY KEY(AdvertisementID),
  FOREIGN KEY(AdvertisementID) REFERENCES Advertisement(AdvertisementID)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Visit (
  UserID INT,
  AdvertisementID INT,
  PRIMARY KEY(UserID, AdvertisementID),
  FOREIGN KEY(UserID) REFERENCES NormalUser(PubID),
  FOREIGN KEY(AdvertisementID) REFERENCES Advertisement(AdvertisementID)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Modified (
  AdminID INT,
  AdvertisementID INT,
  PRIMARY KEY(AdminID, AdvertisementID),
  FOREIGN KEY(AdminID) REFERENCES Administrator(AdminID),
  FOREIGN KEY(AdvertisementID) REFERENCES Advertisement(AdvertisementID)
);


INSERT INTO AdCategory(CatID, CatName) VALUES (0, 'Other');
INSERT INTO AdCategory(CatID, CatName) VALUES (1, 'HomeAppliance');
INSERT INTO AdCategory(CatID, CatName) VALUES (2, 'Vehicle');
INSERT INTO AdCategory(CatID, CatName) VALUES (3, 'RealState');
INSERT INTO AdCategory(CatID, CatName) VALUES (4, 'DigitalProduct');

INSERT INTO StatusState(AdStateID, AdStateName) VALUES (0, 'PENDING');
INSERT INTO StatusState(AdStateID, AdStateName) VALUES (1, 'ACCEPTED');
INSERT INTO StatusState(AdStateID, AdStateName) VALUES (2, 'REJECTED');

INSERT INTO ReportCategory(CatID, CatName) VALUES (0, 'Offensive');
INSERT INTO ReportCategory(CatID, CatName) VALUES (1, 'WTF is this');
INSERT INTO ReportCategory(CatID, CatName) VALUES (2, 'Not Accurate');
INSERT INTO ReportCategory(CatID, CatName) VALUES (3, 'Bad Word');
INSERT INTO ReportCategory(CatID, CatName) VALUES (4, 'Not Good');

INSERT INTO BusinessCategory(CatID, CatName) VALUES (0, 'Electronics');
INSERT INTO BusinessCategory(CatID, CatName) VALUES (1, 'Jewelry');
INSERT INTO BusinessCategory(CatID, CatName) VALUES (2, 'Toys');
INSERT INTO BusinessCategory(CatID, CatName) VALUES (3, 'Music');
INSERT INTO BusinessCategory(CatID, CatName) VALUES (4, 'Tools');
INSERT INTO BusinessCategory(CatID, CatName) VALUES (5, 'Clothing');
INSERT INTO BusinessCategory(CatID, CatName) VALUES (6, 'Sports');
