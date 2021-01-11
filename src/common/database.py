import logging
import os

import boto3
import mysql.connector
import mysql.connector.pooling

logger = logging.getLogger(__name__)


def get_mysql_password():
    secrets_manager = boto3.client("secretsmanager")
    return secrets_manager.get_secret_value(
        SecretId=os.environ["RDS_PASSWORD_SECRET_NAME"]
    )["SecretString"]


def get_connection(args):
    global logger

    script_dir = os.path.dirname(__file__)
    rel_path = "AmazonRootCA1.pem"
    abs_file_path = os.path.join(script_dir, rel_path)

    logger.info(f"Path to the CR cert is '{abs_file_path}'")

    skip_ssl = args["skip_ssl"] if "skip_ssl" in args else ("SKIP_SSL" not in os.environ)

    logger.info(f"skip_ssl variable: {skip_ssl}")

    return mysql.connector.connect(
        host=args["rds_endpoint"]
        if "rds_endpoint" in args
        else os.environ["RDS_ENDPOINT"],
        user=args["rds_username"]
        if "rds_username" in args
        else os.environ["RDS_USERNAME"],
        password=args["rds_password"]
        if "rds_password" in args
        else get_mysql_password(),
        database=args["rds_database_name"]
        if "rds_database_name" in args
        else os.environ["RDS_DATABASE_NAME"],
        ssl_ca=abs_file_path,
        ssl_verify_cert=False if skip_ssl else True,

    )


def execute_statement(sql, connection):
    cursor = connection.cursor()
    cursor.execute(sql)
    logger.info("Executed: {}".format(sql))
    connection.commit()


def execute_multiple_statements(sql, connection):
    global logger

    cursor = connection.cursor()
    results = cursor.execute(sql, multi=True)
    for result in results:
        if result.with_rows:
            logger.info("Executed: {}".format(result.statement))
        else:
            logger.info(
                "Executed: {}, Rows affected: {}".format(
                    result.statement, result.rowcount
                )
            )
    connection.commit()
