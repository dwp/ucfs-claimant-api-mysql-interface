# DO NOT USE THIS REPO - MIGRATED TO GITLAB

# ucfs-claimant-api-mysql-interface

## AWS lambda to provide an interface with the UCFS Claimant API database.

After cloning this repo, please run:  
`make bootstrap`

This lambda is used to load data from a stage environment in to the production environment for the Claimant API mysql database. It is no longer used due to Claimant API being completely switched over in live to a streaming platform now.

## Process

The lambda performs the following to load data from stage, replacing the existing data:

1. Drop a temp table if exists
2. Create the temp table again from the staging table
3. Rename the main table to `_old`
4. Rename the temp table to the main table

## Triggering

To trigger the lambda, you need to provide it a payload like this:

{
  "environment": "dev",
  "application": "dev",
  "rds_endpoint": "localhost",
  "rds_username": "root",
  "rds_database_name": "db_name",
  "rds_password_secret_name": "secret_name",
  "rds_password": "password",
  "skip_ssl": true
}

## Testing

There are tox unit tests in the module. To run them, you will need the module tox installed with `pip install tox`, 
then go to the root of the module and simply run `tox` to run all the unit tests.

**You should always ensure they work before making a pull request for your branch.**

**If tox has an issue with Python version you have installed, you can specify such as `tox -e py38`.**
