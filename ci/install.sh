#!/bin/sh

# libevent development files are required for gevent
apt-get install libevent-dev

# Install GeoDjango dependencies -- see
# https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/#ubuntu
apt-get install binutils gdal-bin libproj-dev postgresql-9.1-postgis \
        postgresql-server-dev-9.1 python-psycopg2

virtualenv .env
source .env/bin/activate

echo "Install the python requirements"
pip install -r requirements.txt

echo "... and this, optional testing stuff"
pip install coverage


psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis';"
POSTGIS_SQL_PATH=`pg_config --sharedir`/contrib/postgis-1.5
psql -d template_postgis -f $POSTGIS_SQL_PATH/postgis.sql # Loading the PostGIS SQL routines
psql -d template_postgis -f $POSTGIS_SQL_PATH/spatial_ref_sys.sql
psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;" # Enabling users to alter spatial tables.
psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"

createdb -T template_postgis councilmatic

echo "Create the database"
psql -U postgres <<EOF
    CREATE USER councilmatic WITH PASSWORD 'councilmatic';
    CREATE DATABASE councilmatic WITH TEMPLATE = template_postgis;
    GRANT ALL ON DATABASE template_postgis TO councilmatic;
    GRANT ALL ON DATABASE councilmatic TO councilmatic;
    ALTER USER councilmatic WITH CREATEDB;

exit #to return to your normal user
----------------------------------- 

cp councilmatic/oakland_local_settings.py.template councilmatic/local_settings.py
