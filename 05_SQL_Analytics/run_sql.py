from __future__ import annotations

import sys
from pathlib import Path

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = (
    PROJECT_ROOT
    / "03_Data_Generation"
    / "output"
    / "v1.0"
)

REPORT_DIR = (
    PROJECT_ROOT
    / "05_SQL_Analytics"
    / "reports"
)

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def run_sql(
    sql_filename: str,
    output_filename: str,
) -> None:

    sql_file = (
        PROJECT_ROOT
        / "05_SQL_Analytics"
        / "sql"
        / sql_filename
    )

    sql = sql_file.read_text(
        encoding="utf-8"
    )

    sql = sql.replace(
        "${DATA_DIR}",
        str(DATA_DIR).replace("\\", "/"),
    )

    connection = duckdb.connect()

    dataframe = connection.execute(
        sql
    ).df()

    output_file = (
        REPORT_DIR
        / output_filename
    )

    dataframe.to_csv(
        output_file,
        index=False,
    )

    print(
        dataframe.to_string(
            index=False
        )
    )

    print(
        f"\nSaved: {output_file}"
    )

    connection.close()


def main() -> None:

    if len(sys.argv) != 3:
        raise SystemExit(
            "Usage: python run_sql.py "
            "<sql_file> <output_csv>"
        )

    run_sql(
        sql_filename=sys.argv[1],
        output_filename=sys.argv[2],
    )


if __name__ == "__main__":
    main()
