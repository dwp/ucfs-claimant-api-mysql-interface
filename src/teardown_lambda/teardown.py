import json
import os
import multiprocessing

from common import common, database

logger = None

base_copy_query = """
CREATE TABLE IF NOT EXISTS {table}_stage LIKE {table}_old;
INSERT INTO {table}_stage (id, data) SELECT id, data from {table}_old;
"""

# Copy tables
copy_queries = [
    # Claimant
    base_copy_query.replace("{table}", "claimant"),
    # Contract
    base_copy_query.replace("{table}", "contract"),
    # Statement
    base_copy_query.replace("{table}", "statement"),
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


def execute_query_multiple_statements(query, args):
    query_connection = database.get_connection(args)
    database.execute_multiple_statements(query, query_connection)


def handler(event, context):
    global logger

    try:
        # Empty list means no keys are required
        args = common.get_parameters(event, [])

        logger = common.initialise_logger(args)

        processes = []

        for query in copy_queries:
            p = multiprocessing.Process(
                target=execute_query_multiple_statements,
                args=(
                    query,
                    args,
                ),
            )
            processes.append(p)
            p.start()

        for process in processes:
            process.join()

        connection = database.get_connection(args)
        database.execute_multiple_statements(drop_query, connection)
        database.execute_statement(rename_query, connection)

        return 200
    except Exception as e:
        logger.error("Failed to execute one or more SQL statement(s)")
        logger.error(e)
        return 500


if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)
    rel_path = "../resources"
    abs_file_path = os.path.join(script_dir, rel_path)

    with open(os.path.join(abs_file_path, "event.json"), "r") as file:
        json_content = json.loads(file.read())
        handler(json_content, None)
