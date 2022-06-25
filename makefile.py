import os
import argparse


def run_and_raise_errors(command):
    status_code = os.system(command)
    if status_code != 0:
        raise Exception("Non Zero Status Code exit")


parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("--action", type=str)
args = parser.parse_args()

match args.action:
    case "lint":
        run_and_raise_errors(
            r'black . --check --exclude "^.*\b(migrations)\b.*$|venv\/"'
        )
