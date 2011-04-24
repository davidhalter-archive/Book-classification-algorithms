#!/bin/bash

apt-get install python-django postgresql python-psycopg2

sudo su - postgres -c "createuser `whoami`"
sudo su - postgres -c "createdb sip"

psql sip < schema.sql 
