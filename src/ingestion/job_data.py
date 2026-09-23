import pandas as pd
from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Raw data directory
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def load_csv(file_name):
    """
    Load a CSV file from the raw data directory.
    """
    file_path = RAW_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    return pd.read_csv(file_path)


def profile_dataframe(df, name):
    """
    Display basic data-quality information.
    """

    print("\n" + "=" * 60)
    print(f"DATASET: {name}")
    print("=" * 60)

    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumns:")
    print(list(df.columns))

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    missing = df.isnull().sum()

    if missing.sum() == 0:
        print("No missing values.")
    else:
        print(missing[missing > 0])

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nUnique Values:")
    for column in df.columns:
        print(f"{column}: {df[column].nunique():,}")


def main():

    print("JOB MARKET INTELLIGENCE")
    print("Data Profiling - Raw Dataset")
    print("=" * 60)

    # ---------------------------------------------------------
    # Load datasets
    # ---------------------------------------------------------

    fact_jobs = load_csv("fact_job_postings.csv")
    bridge_skills = load_csv("bridge_job_skills.csv")
    dim_company = load_csv("dim_company.csv")
    dim_country = load_csv("dim_country.csv")
    dim_platform = load_csv("dim_platform.csv")
    dim_skill = load_csv("dim_skill.csv")

    # ---------------------------------------------------------
    # Profile datasets
    # ---------------------------------------------------------

    profile_dataframe(
        fact_jobs,
        "fact_job_postings.csv"
    )

    profile_dataframe(
        bridge_skills,
        "bridge_job_skills.csv"
    )

    profile_dataframe(
        dim_company,
        "dim_company.csv"
    )

    profile_dataframe(
        dim_country,
        "dim_country.csv"
    )

    profile_dataframe(
        dim_platform,
        "dim_platform.csv"
    )

    profile_dataframe(
        dim_skill,
        "dim_skill.csv"
    )

    # ---------------------------------------------------------
    # Additional checks for job postings
    # ---------------------------------------------------------

    print("\n" + "=" * 60)
    print("JOB POSTING QUALITY CHECKS")
    print("=" * 60)

    print("\nDuplicate job IDs:")
    print(
        fact_jobs["job_id"].duplicated().sum()
    )

    print("\nSalary checks:")

    print(
        "Salary min < 0:",
        (fact_jobs["salary_min_usd"] < 0).sum()
    )

    print(
        "Salary max < 0:",
        (fact_jobs["salary_max_usd"] < 0).sum()
    )

    print(
        "Salary min > salary max:",
        (
            fact_jobs["salary_min_usd"]
            > fact_jobs["salary_max_usd"]
        ).sum()
    )

    print("\nRemote option distribution:")
    print(
        fact_jobs["remote_option"].value_counts(dropna=False)
    )

    print("\nExperience level distribution:")
    print(
        fact_jobs["experience_level"].value_counts(dropna=False)
    )

    print("\nEmployment type distribution:")
    print(
        fact_jobs["employment_type"].value_counts(dropna=False)
    )

    print("\nPlatform distribution:")
    print(
        fact_jobs["platform"].value_counts(dropna=False)
    )

    print("\nCountry distribution:")
    print(
        fact_jobs["country"].value_counts().head(20)
    )

    print("\nTop companies:")
    print(
        fact_jobs["company"].value_counts().head(20)
    )

    print("\nTop job titles:")
    print(
        fact_jobs["job_title"].value_counts().head(20)
    )

    print("\nTop skills:")
    print(
        bridge_skills["skill"].value_counts().head(20)
    )

    print("\n" + "=" * 60)
    print("DATA PROFILING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()