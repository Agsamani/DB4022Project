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

3,4
SELECT NU.FirstName, NU.LastName, 
    CONCAT(
        CAST(EXTRACT(YEAR FROM Advertisement.CreationDate) AS VARCHAR(4)),
        '-',
        CAST(EXTRACT(MONTH FROM Advertisement.CreationDate) AS VARCHAR(2))) AS MonthYear, 
        SUM(Advertisement.Price) AS TotalPrice
FROM NormalUser AS NU
JOIN Advertisement ON NU.PubID = Advertisement.PubID
GROUP BY NU.PubID, MonthYear
ORDER BY NU.FirstName, NU.LastName;


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
ORDER BY Cnt DESC LIMIT 3;


--10
SELECT City.CName, (
    SELECT COUNT(Advertisement.AdvertisementID) FROM Advertisement 
    GROUP BY Advertisement.CityID 
    HAVING Advertisement.CityID = City.CityID
) FROM State JOIN City 
ON State.StateID = City.StateID 
WHERE State.SName = 'Tehran';--'New York'


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


--15
SELECT DISTINCT NU.Email
FROM NormalUser NU
WHERE NOT EXISTS (
    SELECT CatID
    FROM AdCategory
    WHERE NOT EXISTS (
        SELECT *
        FROM Advertisement A
        WHERE A.CatID = AdCategory.CatID
        AND A.PubID = NU.PubID
    )
);


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
OFFSET 2;


--18
SELECT CONCAT(FirstName, ' ', LastName), 
    COALESCE(
        CAST((
            SELECT COUNT(Modified.AdvertisementID) FROM Modified 
            WHERE Modified.AdminID = Administrator.AdminID
            AND Modified.ToStateID = 2
            ) AS FLOAT) 
            / 
        NULLIF(
            CAST((
                SELECT COUNT(Modified.AdvertisementID) FROM Modified 
                WHERE Modified.AdminID = Administrator.AdminID
                ) AS FLOAT)
        , 0)
    , 0) * 100.0 AS Percentage
FROM Administrator
ORDER BY(2) LIMIT 1; 


--19 
UPDATE NormalUser
SET LastName = 'Mohammadi'
WHERE PubID IN (
    SELECT Advertisement.PubID FROM Advertisement
    JOIN AdStatus ON Advertisement.AdvertisementID = AdStatus.AdvertisementID
    WHERE AdStatus.AdStateID = 2
    GROUP BY Advertisement.PubID 
    HAVING COUNT(Advertisement.AdvertisementID) >= ALL (
        SELECT COUNT(Advertisement.AdvertisementID) FROM Advertisement
        JOIN AdStatus ON Advertisement.AdvertisementID = AdStatus.AdvertisementID
        WHERE AdStatus.AdStateID = 2
        GROUP BY Advertisement.PubID 
    )
);


--20
DELETE FROM Advertisement
WHERE AdvertisementID IN (
    SELECT Advertisement.AdvertisementID FROM Advertisement
    JOIN AdStatus ON Advertisement.AdvertisementID = AdStatus.AdvertisementID
    JOIN NormalUser ON Advertisement.PubID = NormalUser.PubID
    WHERE Advertisement.CatID = 1 -- Home Aplliance
    AND NormalUser.LastName = 'Mohammadi'
);


--21 
DELETE FROM Advertisement
WHERE Advertisement.AdvertisementID IN (
    SELECT A.AdvertisementID FROM Advertisement A
    JOIN AdStatus ON A.AdvertisementID = AdStatus.AdvertisementID
    WHERE AdStatus.AdStateID = 2
);


--22
SELECT COUNT(Advertisement.AdvertisementID) + 100 AS Count FROM Advertisement
JOIN City ON Advertisement.CityID = City.CityID
JOIN State ON City.StateID = State.StateID
WHERE Advertisement.CreationDate::DATE = (NOW() - INTERVAL '1 DAY')::DATE
AND State.SName = 'Fars';


--23 
SELECT ReportCategory.CatName, COUNT(Report.ReportID) FROM Advertisement
JOIN Report ON Advertisement.AdvertisementID = Report.AdvertisementID
JOIN ReportCategory ON Report.CatID = ReportCategory.CatID
WHERE Advertisement.AdvertisementID = (
    SELECT Advertisement.AdvertisementID FROM Advertisement
    JOIN Report ON Advertisement.AdvertisementID = Report.AdvertisementID
    GROUP BY Advertisement.AdvertisementID
    ORDER BY COUNT(Report.ReportID) DESC
    LIMIT 1
)
GROUP BY ReportCategory.CatID;

-------------------------------------------------------
------------------ Stored Procedures ------------------
-------------------------------------------------------


--1
DROP FUNCTION func1(TEXT, TEXT);

CREATE OR REPLACE FUNCTION func1(i_email TEXT DEFAULT NULL, i_phone TEXT DEFAULT NULL)
   RETURNS TABLE(title VARCHAR(255))
   LANGUAGE plpgsql
  AS
$$
DECLARE 
BEGIN
    IF i_email IS NULL AND i_phone IS NULL THEN 
           RAISE EXCEPTION 'Both email and phone cannot be null';
    END IF;

    RETURN QUERY
    SELECT Advertisement.Title FROM Advertisement 
    JOIN NormalUser ON Advertisement.PubID = NormalUser.PubID
    WHERE NormalUser.Email = i_email OR NormalUser.Phone = i_phone
    ORDER BY Advertisement.CreationDate;
END;
$$;


--2
DROP FUNCTION func2(TEXT, TEXT);

CREATE OR REPLACE FUNCTION func2(i_email TEXT DEFAULT NULL, i_phone TEXT DEFAULT NULL)
   RETURNS TABLE(fullname TEXT)
   LANGUAGE plpgsql
  AS
$$
DECLARE 
    v_AdminID INT;
BEGIN
    IF i_email IS NULL AND i_phone IS NULL THEN 
           RAISE EXCEPTION 'Both email and phone cannot be null';
    END IF;

    SELECT Administrator.AdminID INTO v_AdminID FROM Administrator 
    WHERE Administrator.Email = i_email OR Administrator.Phone = i_phone;

    RETURN QUERY
        SELECT CONCAT(NormalUser.FirstName, ' ', NormalUser.LastName) FROM Advertisement
        JOIN Modified ON Advertisement.AdvertisementID = Modified.AdvertisementID
        JOIN NormalUser ON Advertisement.PubID = NormalUser.PubID
        WHERE Modified.AdminID = v_AdminID
        AND Modified.ToStateID = 2
        GROUP BY(NormalUser.PubID);
END;
$$;


--3
DROP FUNCTION func3(TEXT, TEXT);

CREATE OR REPLACE FUNCTION func3(i_city TEXT, i_cat TEXT)
   RETURNS SETOF Advertisement
   LANGUAGE plpgsql
  AS
$$
DECLARE 
    v_StateID INT;
BEGIN
    SELECT City.StateID INTO v_StateID FROM City 
    WHERE City.CName = i_city LIMIT 1;

    RETURN QUERY
        SELECT Advertisement.* FROM Advertisement
        JOIN AdStatus ON Advertisement.AdvertisementID = AdStatus.AdvertisementID
        JOIN City ON Advertisement.CityID = City.CityID
        WHERE AdStatus.AdStateID = 1
        AND City.StateID = v_StateID;
END;
$$;


--4
DROP FUNCTION func4(TEXT);

CREATE OR REPLACE FUNCTION func4(i_phrase TEXT)
    RETURNS SETOF Advertisement
    LANGUAGE plpgsql
    AS
$$
DECLARE 
BEGIN
    RETURN QUERY
        SELECT Advertisement.* 
        FROM Advertisement
        JOIN NormalUser ON NormalUser.PubID = Advertisement.PubID
        WHERE Advertisement.Title LIKE '%' || i_phrase || '%'
        OR Advertisement.AdDesc LIKE '%' || i_phrase || '%'
        OR NormalUser.FirstName LIKE '%' || i_phrase || '%'
        OR NormalUser.LastName LIKE '%' || i_phrase || '%';
END;
$$;


--5
DROP FUNCTION func5(TEXT, TEXT);

CREATE OR REPLACE FUNCTION func5(i_email TEXT DEFAULT NULL, i_phone TEXT DEFAULT NULL)
   --RETURNS TABLE(fullname TEXT)
   RETURNS SETOF NormalUser
   LANGUAGE plpgsql
  AS
$$
DECLARE 
    v_CityID INT;
BEGIN
    IF i_email IS NULL AND i_phone IS NULL THEN 
           RAISE EXCEPTION 'Both email and phone cannot be null';
    END IF;

    SELECT NormalUser.CityID INTO v_CityID FROM NormalUser 
    WHERE NormalUser.Email = i_email OR NormalUser.Phone = i_phone;

    RETURN QUERY
        SELECT * 
        FROM NormalUser
        WHERE NormalUser.CityID = v_CityID;
END;
$$;


--6
DROP FUNCTION func6(TIMESTAMP, INT);

CREATE OR REPLACE FUNCTION func6(i_date TIMESTAMP, i_n INT)
   RETURNS SETOF NormalUser
   LANGUAGE plpgsql
  AS
$$
DECLARE 
BEGIN
    DROP TABLE IF EXISTS user_result;

    CREATE TEMP TABLE user_result AS
    SELECT NormalUser.PubID FROM Advertisement
    JOIN NormalUser ON Advertisement.PubID = NormalUser.PubID
    WHERE Advertisement.CreationDate >= i_date
    GROUP BY(NormalUser.PubID) 
    ORDER BY(COUNT(Advertisement.AdvertisementID)) DESC
    LIMIT i_n;

    RETURN QUERY
        SELECT NormalUser.* FROM NormalUser 
        JOIN user_result ON user_result.PubID = NormalUser.PubID;
END;
$$;


--7
DROP FUNCTION func7(i_cat TEXT);

CREATE OR REPLACE FUNCTION func7(i_cat TEXT)
   RETURNS SETOF Advertisement
   LANGUAGE plpgsql
  AS
$$
DECLARE 
    v_CatID INT;
BEGIN
    SELECT CatID INTO v_CatID FROM AdCategory 
    WHERE CatName = i_cat;

    IF v_CatID IS NULL THEN
        RAISE EXCEPTION 'Invalid category';
    END IF;

    RETURN QUERY
        SELECT Advertisement.* FROM Advertisement
        JOIN AdStatus ON Advertisement.AdvertisementID = AdStatus.AdvertisementID
        WHERE Advertisement.CatID = v_CatID
        AND AdStatus.AdStateID = 2
        ORDER BY (Advertisement.CreationDate);
END;
$$;

--8
DROP FUNCTION func8(i_cat TEXT);

CREATE OR REPLACE FUNCTION func8(i_cat TEXT)
   RETURNS SETOF NormalUser
   LANGUAGE plpgsql
  AS
$$
DECLARE 
    v_CatID INT DEFAULT NULL;
BEGIN
    SELECT ReportCategory.CatID INTO v_CatID FROM ReportCategory
    WHERE ReportCategory.CatName = i_cat;

    IF v_CatID IS NULL THEN
        RAISE EXCEPTION 'Invalid category';
    END IF;

    RETURN QUERY
        SELECT NormalUser.* FROM Advertisement
        JOIN Report ON Advertisement.AdvertisementID = Report.AdvertisementID
        JOIN NormalUser ON Advertisement.PubID = NormalUser.PubID
        WHERE Report.CatID = v_CatID
        GROUP BY NormalUser.PubID;
END;
$$;