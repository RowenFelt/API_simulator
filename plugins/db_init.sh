#!/bin/bash

pg_ctl -D ./data initdb 
pg_ctl -D ./data -l logfile start
pg_ctl start -l logfile
