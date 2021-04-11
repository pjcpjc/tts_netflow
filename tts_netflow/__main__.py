# when run from the command line, will read/write json/xls/csv/db/sql/mdb files
from ticdat import standard_main
from tts_netflow import input_schema, solution_schema, solve
if __name__ == "__main__":
    standard_main(input_schema, solution_schema, solve)
