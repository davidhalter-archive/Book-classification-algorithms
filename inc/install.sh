#!/bin/bash

apt-get install python-django postgresql

sudo su - postgres -c "createuser `whoami`"
sudo su - postgres -c "createdb sip"

psql sip < schema.sql 
