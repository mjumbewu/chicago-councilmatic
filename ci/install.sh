#!/bin/sh

# libevent development files are required for gevent
sudo apt-get install libevent-dev

# Install GeoDjango dependencies -- see
# https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/#ubuntu
sudo apt-get install binutils gdal-bin libproj-dev postgresql-9.1-postgis \
     postgresql-server-dev-9.1 python-psycopg2

echo "Install the python requirements"
sudo pip install -r requirements.txt

echo "Install the non-python requirements"
sudo apt-get install poppler-utils

echo "... and this, optional testing stuff"
sudo pip install coverage

# Create a PostGIS template database
psql -c "CREATE DATABASE template_postgis;" -U postgres
psql -c "UPDATE pg_database SET datistemplate='true' WHERE datname='template_postgis';" -U postgres
createlang plpgsql template_postgis -U postgres
# Loading the PostGIS SQL routines
psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql -q
psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql -q
# Enabling users to alter spatial tables.
psql -d template_postgis -c "GRANT ALL ON geometry_columns TO PUBLIC;"
psql -d template_postgis -c "GRANT ALL ON geography_columns TO PUBLIC;"
psql -d template_postgis -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;"

echo "Create the database"
psql -U postgres <<EOF
    CREATE USER councilmatic WITH PASSWORD 'councilmatic';
    CREATE DATABASE councilmatic WITH TEMPLATE = template_postgis;
    GRANT ALL ON DATABASE template_postgis TO councilmatic;
    GRANT ALL ON DATABASE councilmatic TO councilmatic;
    ALTER USER councilmatic WITH CREATEDB;
EOF

echo "Initialize the project settings"
cp councilmatic/local_settings.py.template councilmatic/local_settings.py

echo "Set up logging"
mkdir councilmatic/logs
