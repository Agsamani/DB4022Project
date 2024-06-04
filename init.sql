\! cls
\c postgres

DROP DATABASE IF EXISTS wall;

CREATE DATABASE Wall;
\c wall
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
