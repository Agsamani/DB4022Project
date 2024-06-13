\! cls
\c postgres

DO
$do$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'wolUser') THEN

      DROP OWNED BY woluser;
      DROP DATABASE IF EXISTS woldb;
      DROP USER woluser;
   END IF;
END
$do$;

DROP DATABASE IF EXISTS woldb;
CREATE DATABASE woldb;

CREATE USER wolUser WITH ENCRYPTED PASSWORD '12wol34';
GRANT postgres TO wolUser;


\c woldb
\i 'SqlScripts\\tables.sql'

-- \i 'SqlScripts\\DummyData\\State.sql'
-- \i 'SqlScripts\\DummyData\\City.sql'
-- \i 'SqlScripts\\DummyData\\Administrator.sql'
-- \i 'SqlScripts\\DummyData\\Publisher.sql'
-- \i 'SqlScripts\\DummyData\\NormalUser.sql'
-- \i 'SqlScripts\\DummyData\\Business.sql'
-- \i 'SqlScripts\\DummyData\\Advertisement.sql'
-- \i 'SqlScripts\\DummyData\\AdStatus.sql'
-- \i 'SqlScripts\\DummyData\\Report.sql'
-- \i 'SqlScripts\\DummyData\\HomeAppliance.sql'
-- \i 'SqlScripts\\DummyData\\Vehicle.sql'
-- \i 'SqlScripts\\DummyData\\RealEstate.sql'
-- \i 'SqlScripts\\DummyData\\DigitalProduct.sql'
-- \i 'SqlScripts\\DummyData\\Other.sql'
-- \i 'SqlScripts\\DummyData\\Visit.sql'
-- \i 'SqlScripts\\DummyData\\Modified.sql'
