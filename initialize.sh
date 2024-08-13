#!/bin/sh
echo "Building server image and launching client..."
docker compose up -d dash
echo 'Press enter to continue...'; 
read ans
