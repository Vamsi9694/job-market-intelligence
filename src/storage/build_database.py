"""
JOB MARKET INTELLIGENCE
Database Storage Layer

Purpose:
    Load processed analytical datasets into a
    SQLite database for SQL analysis and Power BI.

Input:
    data/processed/*.csv

Output:
    data/job_market_intelligence.db
"""

import os
import sqlite3
import pandas as pd


# ============================================================
# 1. CONFIGURATION
# ============================================================

DATA_DIR = "data/processed"

DATABASE_FILE = (
    "data/job_market_intelligence.db"
)


# ============================================================
# 2. DATASETS TO LOAD
# ============================================================

DATASETS = {

    "job_postings_analysis":
        "job_postings_analysis.csv",

    "skill_demand":
        "skill_demand.csv",

    "country_job_summary":
        "country_job_summary.csv",

    "role_summary":
        "role_summary.csv",

    "company_summary":
        "company_summary.csv",

    "platform_summary":
        "platform_summary.csv",

    "remote_summary":
        "remote_summary.csv",

    "experience_summary":
        "experience_summary.csv",
}


# ============================================================
# 3. LOAD CSV
# ============================================================

def load_csv(filename):
    """
    Load a processed CSV dataset.
    """

    file_path = os.path.join(
        DATA_DIR,
        filename
    )

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    print(
        f"Loading: {file_path}"
    )

    df = pd.read_csv(file_path)

    print(
        f"Rows: {len(df):,}"
    )

    print(
        f"Columns: {len(df.columns)}"
    )

    return df


# ============================================================
# 4. CREATE DATABASE CONNECTION
# ============================================================

def create_connection():
    """
    Create SQLite database connection.
    """

    database_directory = os.path.dirname(
        DATABASE_FILE
    )

    if database_directory:

        os.makedirs(
            database_directory,
            exist_ok=True
        )

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    return connection


# ============================================================
# 5. LOAD DATA INTO DATABASE
# ============================================================

def load_dataset_to_database(
    connection,
    table_name,
    df
):
    """
    Write a DataFrame to a SQLite table.
    """

    print(
        f"\nCreating table: {table_name}"
    )

    df.to_sql(
        table_name,
        connection,
        if_exists="replace",
        index=False
    )

    print(
        f"Inserted rows: {len(df):,}"
    )


# ============================================================
# 6. VERIFY TABLE
# ============================================================

def verify_table(
    connection,
    table_name
):
    """
    Verify row count in database table.
    """

    query = (
        f"SELECT COUNT(*) "
        f"FROM {table_name}"
    )

    result = connection.execute(
        query
    ).fetchone()

    row_count = result[0]

    print(
        f"Verified rows: {row_count:,}"
    )

    return row_count


# ============================================================
# 7. LIST DATABASE TABLES
# ============================================================

def list_tables(connection):
    """
    Display all tables in the database.
    """

    query = """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
    """

    tables = pd.read_sql_query(
        query,
        connection
    )

    print("\nDatabase tables:")

    for table in tables["name"]:

        print(
            f"  - {table}"
        )

    return tables


# ============================================================
# 8. DATABASE SUMMARY
# ============================================================

def database_summary(connection):
    """
    Display database table statistics.
    """

    print("\n")
    print("=" * 70)
    print("DATABASE SUMMARY")
    print("=" * 70)

    tables = list_tables(
        connection
    )

    print("\nTable row counts:")

    for table in tables["name"]:

        query = (
            f"SELECT COUNT(*) "
            f"FROM {table}"
        )

        count = connection.execute(
            query
        ).fetchone()[0]

        print(
            f"  {table}: {count:,}"
        )


# ============================================================
# 9. MAIN DATABASE BUILD
# ============================================================

def build_database():

    print("=" * 70)
    print("JOB MARKET INTELLIGENCE")
    print("DATABASE BUILD")
    print("=" * 70)

    print(
        f"\nDatabase: {DATABASE_FILE}"
    )

    # --------------------------------------------------------
    # Create connection
    # --------------------------------------------------------

    connection = create_connection()

    try:

        # ----------------------------------------------------
        # Load each analytical dataset
        # ----------------------------------------------------

        for table_name, filename in DATASETS.items():

            df = load_csv(
                filename
            )

            load_dataset_to_database(
                connection,
                table_name,
                df
            )

            verify_table(
                connection,
                table_name
            )

        # ----------------------------------------------------
        # Commit changes
        # ----------------------------------------------------

        connection.commit()

        # ----------------------------------------------------
        # Final database summary
        # ----------------------------------------------------

        database_summary(
            connection
        )

    finally:

        connection.close()

    # --------------------------------------------------------
    # Completion message
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("DATABASE BUILD COMPLETE")
    print("=" * 70)

    print(
        f"\nSQLite database created at:"
    )

    print(
        DATABASE_FILE
    )


# ============================================================
# 10. RUN
# ============================================================

if __name__ == "__main__":

    build_database()