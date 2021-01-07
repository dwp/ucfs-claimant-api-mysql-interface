import json
import logging
import os
import socket
import sys

import boto3


def initialise_logger(args):
    try:
        return setup_logging(
            os.environ["LOG_LEVEL"] if "LOG_LEVEL" in os.environ else "INFO",
            args["environment"] if "environment" in args else os.environ["ENVIRONMENT"],
            args["application"] if "application" in args else os.environ["APPLICATION"],
        )
    except KeyError as e:
        print(
            f"CRITICAL failed to configure logging, environment variable {e.args[0]} missing"
        )
        raise e


def setup_logging(logger_level, environment, application):
    """Set the default logger with json output."""
    the_logger = logging.getLogger()
    for old_handler in the_logger.handlers:
        the_logger.removeHandler(old_handler)

    new_handler = logging.StreamHandler(sys.stdout)

    hostname = socket.gethostname()

    json_format = (
        '{ "timestamp": "%(asctime)s", "log_level": "%(levelname)s", "message": "%(message)s", '
        f'"environment": "{environment}","application": "{application}", '
        f'"module": "%(module)s", "process":"%(process)s", '
        f'"thread": "[%(thread)s]", "hostname": "{hostname}"}}'
    )

    new_handler.setFormatter(logging.Formatter(json_format))
    the_logger.addHandler(new_handler)
    new_level = logging.getLevelName(logger_level.upper())
    the_logger.setLevel(new_level)

    if the_logger.isEnabledFor(logging.DEBUG):
        # Log everything from boto3
        boto3.set_stream_logger()
        the_logger.debug(f'Using boto3", "version": "{boto3.__version__}')

    return the_logger


def get_parameters(event, required_keys):
    logger = logging.getLogger(__name__)
    logger.info(f"Event: {json.dumps(event)}")

    _args = event

    # Add environment variables to arguments where set
    if "AWS_PROFILE" in os.environ:
        _args["aws_profile"] = os.environ["AWS_PROFILE"]

    if "AWS_REGION" in os.environ:
        _args["aws_region"] = os.environ["AWS_REGION"]

    if "ENVIRONMENT" in os.environ:
        _args["environment"] = os.environ["ENVIRONMENT"]

    if "APPLICATION" in os.environ:
        _args["application"] = os.environ["APPLICATION"]

    if "RDS_ENDPOINT" in os.environ:
        _args["rds_endpoint"] = os.environ["RDS_ENDPOINT"]

    if "RDS_USERNAME" in os.environ:
        _args["rds_username"] = os.environ["RDS_USERNAME"]

    if "RDS_DATABASE_NAME" in os.environ:
        _args["rds_database_name"] = os.environ["RDS_DATABASE_NAME"]

    if "RDS_PASSWORD_SECRET_NAME" in os.environ:
        _args["rds_password_secret_name"] = os.environ["RDS_PASSWORD_SECRET_NAME"]

    required_env_vars = [
        "environment",
        "application",
        "rds_endpoint",
        "rds_username",
        "rds_database_name",
        "rds_password_secret_name",
    ]

    # Validate event and environment variables
    missing_event_keys = []
    for required_arg in required_keys + required_env_vars:
        if required_arg not in _args:
            missing_event_keys.append(required_arg)
    if missing_event_keys:
        raise KeyError(
            "KeyError: The following keys are missing from the event or env vars: {}".format(
                ", ".join(missing_event_keys)
            )
        )

    logger.info(f"Args: {json.dumps(_args)}")
    return _args
