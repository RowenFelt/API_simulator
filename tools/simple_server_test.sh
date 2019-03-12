#!/bin/bash

curl --header "Content-Type: application/json" \
  --request GET \
  --data '{"username":"xyz","password":"xyz"}' \
  http://localhost:5000/api/login
