import json
import os

from common import initialise_logger, get_parameters, get_connection, execute_statement, execute_multiple_statements

logger = None


def handler(event, context):
    global logger

    args = get_parameters(event, [])  # Empty list means no keys are required

    logger = initialise_logger(args)

    # Copy tables
    # TODO: Potential issue with NULL data being copied from empty table
    copy_queries = [
        # Claimant
        """
        CREATE TABLE IF NOT EXISTS claimant_stage LIKE claimant_old;
        INSERT INTO claimant_stage (id, data) SELECT id, data from claimant_old;
        """,

        # Contract
        """
        CREATE TABLE IF NOT EXISTS contract_stage LIKE contract_old;
        INSERT contract_stage (id, data) SELECT id, data from contract_old;
        """,

        # Statement
        """
        CREATE TABLE IF NOT EXISTS statement_stage LIKE statement_old;
        INSERT statement_stage (id, data) SELECT id, data from statement_old;
        """
    ]

    # Drop in-use tables
    drop_query = """
    DROP TABLE IF EXISTS claimant;
    DROP TABLE IF EXISTS contract;
    DROP TABLE IF EXISTS statement;
    """

    # Remove _stage suffixes
    rename_query = """
    RENAME TABLE claimant_stage TO claimant,
                 contract_stage TO contract,
                 statement_stage TO statement;
    """

    connection = get_connection(args)

    for query in copy_queries:
        execute_multiple_statements(query, connection)

    execute_multiple_statements(drop_query, connection)
    execute_statement(rename_query, connection)

    return "OK"  # TODO: Change this response in future


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    rel_path = "../resources"
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(os.path.join(abs_file_path, "event.json"), "r") as file:
        json_content = json.loads(file.read())
        handler(json_content, None)
