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
\i 'tables.sql'

\i 'DummyData\\State.sql'
\i 'DummyData\\City.sql'
\i 'DummyData\\Administrator.sql'
\i 'DummyData\\Publisher.sql'
\i 'DummyData\\NormalUser.sql'
\i 'DummyData\\Business.sql'
\i 'DummyData\\Advertisement.sql'
\i 'DummyData\\AdStatus.sql'
\i 'DummyData\\Report.sql'
\i 'DummyData\\HomeAppliance.sql'
\i 'DummyData\\Vehicle.sql'
\i 'DummyData\\RealEstate.sql'
\i 'DummyData\\DigitalProduct.sql'
\i 'DummyData\\Other.sql'
\i 'DummyData\\Visit.sql'
\i 'DummyData\\Modified.sql'
