--1
SELECT FirstName, LastName FROM NormalUser 
LEFT JOIN (
    SELECT Publisher.PubID, COUNT(Publisher.PubID) AS AdCount FROM 
    Publisher JOIN Advertisement 
    ON Publisher.PubID = Advertisement.PubID
    GROUP BY Publisher.PubID
) AS S
ON S.PubID = NormalUser.PubID
WHERE S.AdCount IS NULL;


--2
SELECT FirstName, LastName FROM 
NormalUser JOIN (
    SELECT UserID FROM Business GROUP BY UserID
) AS S ON NormalUser.PubID = S.UserID;


--5
SELECT NormalUser.PubID FROM NormalUser
WHERE (
    SELECT COALESCE(MAX(S.AdCountPerCity), 0) AS MC FROM (
        SELECT COUNT(*) AS AdCountPerCity FROM 
        Advertisement JOIN City ON Advertisement.CityID = City.CityID 
        WHERE Advertisement.PubID = NormalUser.PubID
        GROUP BY(City.CityID)
    ) AS S
) < 2; 


--6
SELECT NormalUser.* FROM 
NormalUser JOIN Advertisement 
ON NormalUser.PubID = Advertisement.PubID 
ORDER BY Advertisement.CreationDate DESC LIMIT 1;

SELECT * FROM NormalUser
WHERE
(SELECT AVG(Advertisement.Price) FROM Advertisement WHERE Advertisement.PubID = NormalUser.PubID)
 > (SELECT AVG(Advertisement.Price) FROM Advertisement);


--7
SELECT 
    CASE
    WHEN NormalUser.Email IS NULL THEN NormalUser.Phone
    ELSE NormalUser.Email
    END AS Cred
FROM NormalUser JOIN (
    SELECT Advertisement.PubID, AVG(Advertisement.Price) FROM Advertisement 
    GROUP BY Advertisement.PubID
    HAVING AVG(Advertisement.Price) > (
        SELECT AVG(Advertisement.Price) FROM Advertisement
    )
) AS S
ON NormalUser.PubID = S.PubID;


--8 
SELECT CatName, S.AdCount FROM AdCategory JOIN (
    SELECT Advertisement.CatID, COUNT(Advertisement.AdvertisementID) AS AdCount
    FROM Advertisement
    GROUP BY Advertisement.CatID
) AS S ON S.CatID = AdCategory.CatID;


--9
SELECT Advertisement.PubID, COUNT(Advertisement.AdvertisementID) AS Cnt 
FROM Advertisement WHERE
Advertisement.CreationDate BETWEEN NOW() - INTERVAL '7 DAY' AND NOW()
GROUP BY Advertisement.PubID
ORDER BY Cnt DESC LIMIT 3


--10
SELECT City.CName, (
    SELECT COUNT(Advertisement.AdvertisementID) FROM Advertisement 
    GROUP BY Advertisement.CityID 
    HAVING Advertisement.CityID = City.CityID
) FROM State JOIN City 
ON State.StateID = City.StateID 
WHERE State.SName = 'Tehran'--'New York'


--11
SELECT * FROM City WHERE City.CityID IN (
    SELECT Advertisement.CityID FROM Advertisement 
    WHERE Advertisement.PubID = (
        SELECT NormalUser.PubID FROM NormalUser JOIN Publisher 
        ON NormalUser.PubID = Publisher.PubID 
        ORDER BY Publisher.RegDate LIMIT 1
    )
);


--12
SELECT CONCAT(FirstName, ' ', LastName) FROM Administrator;

--13
SELECT * FROM NormalUser JOIN (
    SELECT Advertisement.PubID FROM Advertisement JOIN AdStatus 
    ON Advertisement.AdvertisementID = AdStatus.AdvertisementID 
    WHERE AdStatus.AdStateID = 1 -- 1 Means ACCEPTED
    GROUP BY Advertisement.PubID
    HAVING COUNT(Advertisement.AdvertisementID) >= 2
) AS S ON S.PubID = NormalUser.PubID;


--14
SELECT * FROM NormalUser JOIN (
    SELECT Advertisement.PubID FROM Advertisement JOIN DigitalProduct 
    ON Advertisement.AdvertisementID = DigitalProduct.AdvertisementID 
    GROUP BY Advertisement.PubID
    HAVING COUNT(Advertisement.AdvertisementID) <= 2
) AS S ON S.PubID = NormalUser.PubID;


--16
SELECT * FROM Advertisement 
WHERE CAST(Advertisement.CreationDate AS DATE) = CAST(NOW() AS DATE) 
ORDER BY Advertisement.CreationDate DESC;


--17 ------------------faulty
SELECT Advertisement.AdvertisementID, COUNT(Advertisement.AdvertisementID) FROM 
Advertisement JOIN Visit ON Advertisement.AdvertisementID = Visit.AdvertisementID
GROUP BY Advertisement.AdvertisementID
ORDER BY COUNT(Advertisement.AdvertisementID) DESC
LIMIT 1
OFFSET 2


18
SELECT CONCAT(FirstName, ' ', LastName), 
    COALESCE(
        CAST((
            SELECT COUNT(Advertisement.AdvertisementID) FROM Modified 
            JOIN Advertisement ON Modified.AdvertisementID = Advertisement.AdvertisementID 
            JOIN AdStatus ON Advertisement.AdvertisementID = AdStatus.AdvertisementID
            WHERE Modified.AdminID = Administrator.AdminID
            AND AdStatus.AdStateID = 2
            ) AS FLOAT) 
            / 
        NULLIF(
            CAST((
                SELECT COUNT(Advertisement.AdvertisementID) FROM Modified 
                JOIN Advertisement ON Modified.AdvertisementID = Advertisement.AdvertisementID 
                JOIN AdStatus ON Advertisement.AdvertisementID = AdStatus.AdvertisementID
                WHERE Modified.AdminID = Administrator.AdminID
                ) AS FLOAT)
        , 0)
    , 0) * 100.0 AS Percentage
FROM Administrator
ORDER BY(2) DESC LIMIT 1; 