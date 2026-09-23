"""
Job Market Intelligence
Data Cleaning and Transformation Module

Purpose:
    - Load raw job posting data
    - Clean and standardize fields
    - Validate salary information
    - Preserve malformed posting-date values for traceability
    - Create analytical salary metrics
    - Save the processed dataset

Input:
    data/raw/fact_job_postings.csv

Output:
    data/processed/fact_job_postings_clean.csv
"""

import os
import pandas as pd


# ============================================================
# 1. LOAD DATA
# ============================================================

def load_data(input_file):
    """
    Load raw job posting data from CSV.
    """

    print("=" * 60)
    print("JOB MARKET INTELLIGENCE - DATA CLEANING")
    print("=" * 60)

    print("\nLoading data...")
    print(f"Input file: {input_file}")

    df = pd.read_csv(input_file)

    print(f"Rows loaded: {len(df):,}")
    print(f"Columns loaded: {len(df.columns)}")

    return df


# ============================================================
# 2. CLEAN JOB POSTINGS
# ============================================================

def clean_job_postings(input_file, output_file):
    """
    Clean and transform the raw job postings dataset.
    """

    # --------------------------------------------------------
    # Load dataset
    # --------------------------------------------------------

    df = load_data(input_file)

    print("\n" + "=" * 60)
    print("STARTING DATA CLEANING")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. Remove completely empty rows
    # --------------------------------------------------------

    initial_rows = len(df)

    df = df.dropna(how="all")

    removed_empty_rows = initial_rows - len(df)

    print("\n1. Empty row check")
    print(f"Empty rows removed: {removed_empty_rows}")

    # --------------------------------------------------------
    # 2. Clean column names
    # --------------------------------------------------------

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    print("\n2. Column names standardized")

    # --------------------------------------------------------
    # 3. Clean text columns
    # --------------------------------------------------------

    text_columns = [
        "job_id",
        "job_title",
        "company",
        "country",
        "region",
        "platform",
        "experience_level",
        "employment_type",
        "remote_option"
    ]

    for column in text_columns:

        if column in df.columns:
            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

    print("\n3. Text fields cleaned")

    # --------------------------------------------------------
    # 4. Clean numeric columns
    # --------------------------------------------------------

    numeric_columns = [
        "salary_min_usd",
        "salary_max_usd",
        "applicants_estimate"
    ]

    for column in numeric_columns:

        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    print("\n4. Numeric fields converted")

    # --------------------------------------------------------
    # 5. Remove duplicate job IDs
    # --------------------------------------------------------

    duplicate_job_ids = df["job_id"].duplicated().sum()

    print("\n5. Duplicate job ID check")
    print(f"Duplicate job IDs found: {duplicate_job_ids}")

    if duplicate_job_ids > 0:
        df = df.drop_duplicates(
            subset=["job_id"],
            keep="first"
        )

        print(
            f"Duplicate records removed: {duplicate_job_ids}"
        )
    else:
        print("No duplicate job IDs found.")

    # --------------------------------------------------------
    # 6. Validate salary fields
    # --------------------------------------------------------

    print("\n6. Salary validation")

    negative_min = (
        df["salary_min_usd"] < 0
    ).sum()

    negative_max = (
        df["salary_max_usd"] < 0
    ).sum()

    invalid_salary_range = (
        df["salary_min_usd"] >
        df["salary_max_usd"]
    ).sum()

    print(f"Negative minimum salaries: {negative_min}")
    print(f"Negative maximum salaries: {negative_max}")
    print(
        f"Minimum salary greater than maximum: "
        f"{invalid_salary_range}"
    )

    # Remove impossible salary records
    if negative_min > 0:
        df.loc[
            df["salary_min_usd"] < 0,
            "salary_min_usd"
        ] = pd.NA

    if negative_max > 0:
        df.loc[
            df["salary_max_usd"] < 0,
            "salary_max_usd"
        ] = pd.NA

    # --------------------------------------------------------
    # 7. Handle posting date
    # --------------------------------------------------------

    print("\n7. Posting date handling")

    print(
        "Source posting_date contains values such as "
        "'52:59.3' rather than real calendar dates."
    )

    # Preserve original source value
    # for traceability and audit purposes.

    df["posting_date_raw"] = (
        df["posting_date"]
        .astype("string")
        .str.strip()
    )

    # Do not invent dates.
    # The source does not contain reliable calendar dates.

    df["posting_date"] = pd.NaT

    print(
        "Original posting-date values preserved in "
        "'posting_date_raw'."
    )

    print(
        "posting_date set to missing because "
        "a reliable calendar date cannot be derived."
    )

    # --------------------------------------------------------
    # 8. Create average salary
    # --------------------------------------------------------

    print("\n8. Creating average salary")

    df["salary_avg_usd"] = (
        df["salary_min_usd"] +
        df["salary_max_usd"]
    ) / 2

    # --------------------------------------------------------
    # 9. Create salary range
    # --------------------------------------------------------

    print("9. Creating salary range")

    df["salary_range_usd"] = (
        df["salary_max_usd"] -
        df["salary_min_usd"]
    )

    # --------------------------------------------------------
    # 10. Create average salary in thousands
    # --------------------------------------------------------

    print("10. Creating average salary in thousands")

    df["salary_avg_k_usd"] = (
        df["salary_avg_usd"] / 1000
    )

    # --------------------------------------------------------
    # 11. Round salary metrics
    # --------------------------------------------------------

    df["salary_avg_usd"] = (
        df["salary_avg_usd"].round(2)
    )

    df["salary_range_usd"] = (
        df["salary_range_usd"].round(2)
    )

    df["salary_avg_k_usd"] = (
        df["salary_avg_k_usd"].round(2)
    )

    # --------------------------------------------------------
    # 12. Final missing-value check
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("FINAL DATA QUALITY CHECK")
    print("=" * 60)

    print("\nMissing values after cleaning:")

    missing_values = df.isna().sum()

    print(missing_values)

    # --------------------------------------------------------
    # 13. Final duplicate check
    # --------------------------------------------------------

    print("\nDuplicate rows after cleaning:")

    duplicate_rows = df.duplicated().sum()

    print(duplicate_rows)

    # --------------------------------------------------------
    # 14. Final dataset information
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("FINAL DATASET")
    print("=" * 60)

    print(f"Clean rows: {len(df):,}")
    print(f"Clean columns: {len(df.columns)}")

    print("\nFinal columns:")
    print(list(df.columns))

    # --------------------------------------------------------
    # 15. Create output directory
    # --------------------------------------------------------

    output_directory = os.path.dirname(output_file)

    if output_directory:
        os.makedirs(
            output_directory,
            exist_ok=True
        )

    # --------------------------------------------------------
    # 16. Save processed dataset
    # --------------------------------------------------------

    df.to_csv(
        output_file,
        index=False
    )

    print("\n" + "=" * 60)
    print("DATASET SAVED")
    print("=" * 60)

    print(f"\nProcessed dataset saved to:")
    print(output_file)

    # --------------------------------------------------------
    # 17. Cleaning summary
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("DATA CLEANING COMPLETE")
    print("=" * 60)

    return df


# ============================================================
# 3. MAIN PROGRAM
# ============================================================

def main():

    input_file = (
        "data/raw/fact_job_postings.csv"
    )

    output_file = (
        "data/processed/"
        "fact_job_postings_clean.csv"
    )

    clean_job_postings(
        input_file,
        output_file
    )


# ============================================================
# 4. RUN SCRIPT
# ============================================================

if __name__ == "__main__":
    main()