#!/bin/bash

# Ensure that PostgreSQL is installed
if ! command -v psql &> /dev/null
then
    echo "PostgreSQL is not installed. Please install PostgreSQL and try again."
    exit 1
fi

# Check if the script is running with administrative privileges
if [ "$EUID" -ne 0 ]; then
    echo "This script requires administrative privileges. A password will be requested..."
    exec pkexec bash "$0" "$@"
    exit
fi

# PostgreSQL connection information
TARGET_USER=$1      # Username to be created
TARGET_PASSWORD=$2  # Password for the user to be created
DB_USER=$3          # Database superuser
DB_HOST=$4          # Database host
DB_PORT=$5          # Database port

# Read the password from the terminal only once
read -s -p "Please enter the PostgreSQL password: " PGPASSWORD
echo  # Empty line (to create a new line under the password)

if [ -f /home/$USER/.pgpass ]; then
    echo "pgpass file already exists."
else
    echo "pgpass file not found. Creating..."
    echo "$DB_HOST:$DB_PORT:*:$DB_USER:$PGPASSWORD" > /home/$USER/.pgpass
    chmod 600 /home/$USER/.pgpass
    echo "pgpass file successfully created."
fi

# Query to check if the user exists
USER_EXISTS=$(PGPASSWORD="$PGPASSWORD" psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -tAc "SELECT 1 FROM pg_roles WHERE rolname='$TARGET_USER';")

if [ "$USER_EXISTS" == "1" ]; then
    echo "User '$TARGET_USER' already exists."
else
    echo "User '$TARGET_USER' not found. Creating..."
    PGPASSWORD="$PGPASSWORD" psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -c "CREATE USER $TARGET_USER WITH PASSWORD '$TARGET_PASSWORD';"
    echo "User '$TARGET_USER' successfully created."
fi

# Query to check if the user has database creation privileges
HAS_CREATEDB_PRIV=$(PGPASSWORD="$PGPASSWORD" psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -tAc "SELECT 1 FROM pg_roles WHERE rolname='$TARGET_USER' AND rolcreatedb;")

if [ "$HAS_CREATEDB_PRIV" == "1" ]; then
    echo "User '$TARGET_USER' has database creation privileges."
else
    echo "User '$TARGET_USER' does not have database creation privileges. Granting permission..."
    PGPASSWORD="$PGPASSWORD" psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -c "ALTER USER $TARGET_USER CREATEDB;"
    echo "Database creation privileges successfully granted to user '$TARGET_USER'."
fi
