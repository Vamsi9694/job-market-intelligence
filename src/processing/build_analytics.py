"""
JOB MARKET INTELLIGENCE
Analytical Data Processing Layer

Purpose:
    Transform cleaned job-posting data into
    analysis-ready datasets for Python, SQL
    and Power BI.

Input:
    data/processed/fact_job_postings_clean.csv
    data/raw/bridge_job_skills.csv

Outputs:
    data/processed/job_postings_analysis.csv
    data/processed/skill_demand.csv
    data/processed/country_job_summary.csv
    data/processed/role_summary.csv
    data/processed/company_summary.csv
    data/processed/platform_summary.csv
    data/processed/remote_summary.csv
    data/processed/experience_summary.csv
"""

import os
import pandas as pd


# ============================================================
# 1. CONFIGURATION
# ============================================================

JOB_FILE = (
    "data/processed/"
    "fact_job_postings_clean.csv"
)

SKILL_FILE = (
    "data/raw/"
    "bridge_job_skills.csv"
)

OUTPUT_DIR = "data/processed"


# ============================================================
# 2. LOAD DATA
# ============================================================

def load_data():
    """
    Load cleaned job postings and job-skill bridge data.
    """

    print("=" * 70)
    print("JOB MARKET INTELLIGENCE")
    print("ANALYTICAL DATA PROCESSING")
    print("=" * 70)

    print("\nLoading cleaned job postings...")

    if not os.path.exists(JOB_FILE):
        raise FileNotFoundError(
            f"File not found: {JOB_FILE}"
        )

    jobs = pd.read_csv(JOB_FILE)

    print(
        f"Job postings loaded: "
        f"{len(jobs):,}"
    )

    print("\nLoading job-skill bridge...")

    if not os.path.exists(SKILL_FILE):
        raise FileNotFoundError(
            f"File not found: {SKILL_FILE}"
        )

    skills = pd.read_csv(SKILL_FILE)

    print(
        f"Job-skill records loaded: "
        f"{len(skills):,}"
    )

    return jobs, skills


# ============================================================
# 3. STANDARDIZE DATA
# ============================================================

def standardize_data(jobs, skills):
    """
    Standardize column names and text values.
    """

    jobs = jobs.copy()
    skills = skills.copy()

    # --------------------------------------------------------
    # Column names
    # --------------------------------------------------------

    jobs.columns = (
        jobs.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    skills.columns = (
        skills.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # --------------------------------------------------------
    # Job text fields
    # --------------------------------------------------------

    job_text_columns = [
        "job_id",
        "job_title",
        "company",
        "country",
        "region",
        "platform",
        "experience_level",
        "employment_type",
        "remote_option",
    ]

    for column in job_text_columns:

        if column in jobs.columns:

            jobs[column] = (
                jobs[column]
                .astype(str)
                .str.strip()
            )

    # --------------------------------------------------------
    # Skill fields
    # --------------------------------------------------------

    skills["job_id"] = (
        skills["job_id"]
        .astype(str)
        .str.strip()
    )

    skills["skill"] = (
        skills["skill"]
        .astype(str)
        .str.strip()
    )

    return jobs, skills


# ============================================================
# 4. CREATE JOB-LEVEL ANALYTICAL DATASET
# ============================================================

def build_job_analysis(jobs):
    """
    Create one analytical record per job posting.
    """

    print("\n")
    print("=" * 70)
    print("1. BUILDING JOB POSTINGS ANALYSIS")
    print("=" * 70)

    df = jobs.copy()

    # --------------------------------------------------------
    # Salary band
    # --------------------------------------------------------

    def salary_band(value):

        if pd.isna(value):
            return "Unknown"

        if value < 50000:
            return "Under $50K"

        elif value < 75000:
            return "$50K-$75K"

        elif value < 100000:
            return "$75K-$100K"

        elif value < 125000:
            return "$100K-$125K"

        elif value < 150000:
            return "$125K-$150K"

        elif value < 175000:
            return "$150K-$175K"

        else:
            return "$175K+"

    df["salary_band"] = (
        df["salary_avg_usd"]
        .apply(salary_band)
    )

    # --------------------------------------------------------
    # Experience ranking
    # --------------------------------------------------------

    experience_rank = {
        "Entry": 1,
        "Mid": 2,
        "Senior": 3,
        "Lead": 4,
    }

    df["experience_rank"] = (
        df["experience_level"]
        .map(experience_rank)
    )

    # --------------------------------------------------------
    # Remote flag
    # --------------------------------------------------------

    df["is_remote"] = (
        df["remote_option"]
        .eq("Remote")
        .astype(int)
    )

    df["is_hybrid"] = (
        df["remote_option"]
        .eq("Hybrid")
        .astype(int)
    )

    df["is_onsite"] = (
        df["remote_option"]
        .eq("Onsite")
        .astype(int)
    )

    # --------------------------------------------------------
    # Salary spread percentage
    # --------------------------------------------------------

    df["salary_range_pct"] = (
        df["salary_range_usd"]
        / df["salary_avg_usd"]
        * 100
    )

    # --------------------------------------------------------
    # Applicant competition bands
    # --------------------------------------------------------

    def competition_band(value):

        if pd.isna(value):
            return "Unknown"

        if value < 100:
            return "Low"

        elif value < 250:
            return "Moderate"

        elif value < 400:
            return "High"

        else:
            return "Very High"

    df["competition_band"] = (
        df["applicants_estimate"]
        .apply(competition_band)
    )

    # --------------------------------------------------------
    # Job title category
    # --------------------------------------------------------

    def role_category(title):

        title = str(title).lower()

        if "business intelligence" in title:
            return "Business Intelligence"

        elif "data analyst" in title:
            return "Data Analytics"

        elif "analytics engineer" in title:
            return "Analytics Engineering"

        elif "data engineer" in title:
            return "Data Engineering"

        elif "data scientist" in title:
            return "Data Science"

        elif "machine learning" in title:
            return "Machine Learning"

        elif "ai engineer" in title:
            return "AI Engineering"

        else:
            return "Other"

    df["role_category"] = (
        df["job_title"]
        .apply(role_category)
    )

    # --------------------------------------------------------
    # Reorder important analytical fields
    # --------------------------------------------------------

    preferred_columns = [
        "job_id",
        "job_title",
        "role_category",
        "company",
        "country",
        "region",
        "platform",
        "experience_level",
        "experience_rank",
        "employment_type",
        "remote_option",
        "is_remote",
        "is_hybrid",
        "is_onsite",
        "salary_min_usd",
        "salary_max_usd",
        "salary_avg_usd",
        "salary_avg_k_usd",
        "salary_range_usd",
        "salary_range_pct",
        "salary_band",
        "applicants_estimate",
        "competition_band",
        "posting_date",
        "posting_date_raw",
    ]

    existing_columns = [
        column
        for column in preferred_columns
        if column in df.columns
    ]

    remaining_columns = [
        column
        for column in df.columns
        if column not in existing_columns
    ]

    df = df[
        existing_columns
        + remaining_columns
    ]

    print(
        f"Job analysis rows: "
        f"{len(df):,}"
    )

    print(
        f"Job analysis columns: "
        f"{len(df.columns)}"
    )

    return df


# ============================================================
# 5. BUILD SKILL DEMAND DATASET
# ============================================================

def build_skill_demand(skills, jobs):
    """
    Calculate demand for every skill.
    """

    print("\n")
    print("=" * 70)
    print("2. BUILDING SKILL DEMAND")
    print("=" * 70)

    df = skills.copy()

    # --------------------------------------------------------
    # Remove exact duplicates
    # --------------------------------------------------------

    df = df.drop_duplicates(
        subset=["job_id", "skill"]
    )

    # --------------------------------------------------------
    # Count jobs requiring each skill
    # --------------------------------------------------------

    skill_demand = (
        df.groupby("skill")
        .agg(
            job_count=("job_id", "nunique")
        )
        .reset_index()
    )

    # --------------------------------------------------------
    # Calculate percentage of jobs
    # --------------------------------------------------------

    total_jobs = jobs["job_id"].nunique()

    skill_demand["job_percentage"] = (
        skill_demand["job_count"]
        / total_jobs
        * 100
    )

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    skill_demand = (
        skill_demand
        .sort_values(
            "job_count",
            ascending=False
        )
        .reset_index(drop=True)
    )

    # --------------------------------------------------------
    # Rank
    # --------------------------------------------------------

    skill_demand["demand_rank"] = (
        skill_demand.index + 1
    )

    print(
        f"Unique skills: "
        f"{skill_demand['skill'].nunique()}"
    )

    print("\nTop 10 skills:")

    print(
        skill_demand.head(10)
        .to_string(index=False)
    )

    return skill_demand


# ============================================================
# 6. BUILD COUNTRY SUMMARY
# ============================================================

def build_country_summary(jobs):
    """
    Create country-level job market summary.
    """

    print("\n")
    print("=" * 70)
    print("3. BUILDING COUNTRY SUMMARY")
    print("=" * 70)

    summary = (
        jobs.groupby(
            ["country", "region"]
        )
        .agg(
            job_count=("job_id", "nunique"),
            avg_salary_usd=(
                "salary_avg_usd",
                "mean"
            ),
            median_salary_usd=(
                "salary_avg_usd",
                "median"
            ),
            avg_applicants=(
                "applicants_estimate",
                "mean"
            ),
        )
        .reset_index()
    )

    # Remote jobs
    remote_counts = (
        jobs.groupby("country")["is_remote"]
        .sum()
        .reset_index(
            name="remote_job_count"
        )
    )

    summary = summary.merge(
        remote_counts,
        on="country",
        how="left"
    )

    # Remote percentage
    summary["remote_job_percentage"] = (
        summary["remote_job_count"]
        / summary["job_count"]
        * 100
    )

    # Sort
    summary = (
        summary
        .sort_values(
            "job_count",
            ascending=False
        )
        .reset_index(drop=True)
    )

    summary["job_rank"] = (
        summary.index + 1
    )

    print("\nCountry summary:")

    print(
        summary.to_string(index=False)
    )

    return summary


# ============================================================
# 7. BUILD ROLE SUMMARY
# ============================================================

def build_role_summary(jobs):
    """
    Create role-level market summary.
    """

    print("\n")
    print("=" * 70)
    print("4. BUILDING ROLE SUMMARY")
    print("=" * 70)

    summary = (
        jobs.groupby(
            ["job_title", "role_category"]
        )
        .agg(
            job_count=("job_id", "nunique"),
            avg_salary_usd=(
                "salary_avg_usd",
                "mean"
            ),
            median_salary_usd=(
                "salary_avg_usd",
                "median"
            ),
            avg_applicants=(
                "applicants_estimate",
                "mean"
            ),
        )
        .reset_index()
    )

    summary = (
        summary
        .sort_values(
            "job_count",
            ascending=False
        )
        .reset_index(drop=True)
    )

    summary["job_rank"] = (
        summary.index + 1
    )

    print("\nRole summary:")

    print(
        summary.to_string(index=False)
    )

    return summary


# ============================================================
# 8. BUILD COMPANY SUMMARY
# ============================================================

def build_company_summary(jobs):
    """
    Create company-level market summary.
    """

    print("\n")
    print("=" * 70)
    print("5. BUILDING COMPANY SUMMARY")
    print("=" * 70)

    summary = (
        jobs.groupby("company")
        .agg(
            job_count=("job_id", "nunique"),
            avg_salary_usd=(
                "salary_avg_usd",
                "mean"
            ),
            median_salary_usd=(
                "salary_avg_usd",
                "median"
            ),
            avg_applicants=(
                "applicants_estimate",
                "mean"
            ),
        )
        .reset_index()
    )

    # Remote jobs
    remote_counts = (
        jobs.groupby("company")["is_remote"]
        .sum()
        .reset_index(
            name="remote_job_count"
        )
    )

    summary = summary.merge(
        remote_counts,
        on="company",
        how="left"
    )

    summary["remote_job_percentage"] = (
        summary["remote_job_count"]
        / summary["job_count"]
        * 100
    )

    summary = (
        summary
        .sort_values(
            "job_count",
            ascending=False
        )
        .reset_index(drop=True)
    )

    summary["company_rank"] = (
        summary.index + 1
    )

    print("\nTop companies:")

    print(
        summary.head(20)
        .to_string(index=False)
    )

    return summary


# ============================================================
# 9. BUILD PLATFORM SUMMARY
# ============================================================

def build_platform_summary(jobs):
    """
    Create job-platform summary.
    """

    print("\n")
    print("=" * 70)
    print("6. BUILDING PLATFORM SUMMARY")
    print("=" * 70)

    summary = (
        jobs.groupby("platform")
        .agg(
            job_count=("job_id", "nunique"),
            avg_salary_usd=(
                "salary_avg_usd",
                "mean"
            ),
            avg_applicants=(
                "applicants_estimate",
                "mean"
            ),
        )
        .reset_index()
    )

    summary["job_percentage"] = (
        summary["job_count"]
        / summary["job_count"].sum()
        * 100
    )

    summary = (
        summary
        .sort_values(
            "job_count",
            ascending=False
        )
        .reset_index(drop=True)
    )

    summary["platform_rank"] = (
        summary.index + 1
    )

    print(
        summary.to_string(index=False)
    )

    return summary


# ============================================================
# 10. BUILD REMOTE SUMMARY
# ============================================================

def build_remote_summary(jobs):
    """
    Create remote-work summary.
    """

    print("\n")
    print("=" * 70)
    print("7. BUILDING REMOTE SUMMARY")
    print("=" * 70)

    summary = (
        jobs.groupby("remote_option")
        .agg(
            job_count=("job_id", "nunique"),
            avg_salary_usd=(
                "salary_avg_usd",
                "mean"
            ),
            avg_applicants=(
                "applicants_estimate",
                "mean"
            ),
        )
        .reset_index()
    )

    summary["job_percentage"] = (
        summary["job_count"]
        / summary["job_count"].sum()
        * 100
    )

    summary = (
        summary
        .sort_values(
            "job_count",
            ascending=False
        )
        .reset_index(drop=True)
    )

    print(
        summary.to_string(index=False)
    )

    return summary


# ============================================================
# 11. BUILD EXPERIENCE SUMMARY
# ============================================================

def build_experience_summary(jobs):
    """
    Create experience-level summary.
    """

    print("\n")
    print("=" * 70)
    print("8. BUILDING EXPERIENCE SUMMARY")
    print("=" * 70)

    summary = (
        jobs.groupby("experience_level")
        .agg(
            job_count=("job_id", "nunique"),
            avg_salary_usd=(
                "salary_avg_usd",
                "mean"
            ),
            median_salary_usd=(
                "salary_avg_usd",
                "median"
            ),
            avg_applicants=(
                "applicants_estimate",
                "mean"
            ),
        )
        .reset_index()
    )

    experience_order = [
        "Entry",
        "Mid",
        "Senior",
        "Lead",
    ]

    summary["experience_order"] = (
        summary["experience_level"]
        .map(
            {
                level: index
                for index, level
                in enumerate(
                    experience_order
                )
            }
        )
    )

    summary = (
        summary
        .sort_values("experience_order")
        .drop(
            columns=["experience_order"]
        )
        .reset_index(drop=True)
    )

    print(
        summary.to_string(index=False)
    )

    return summary


# ============================================================
# 12. SAVE DATASETS
# ============================================================

def save_dataset(df, filename):
    """
    Save analytical dataset.
    """

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    output_path = os.path.join(
        OUTPUT_DIR,
        filename
    )

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved: {output_path}"
    )


# ============================================================
# 13. FINAL VALIDATION
# ============================================================

def final_validation(
    job_analysis,
    skill_demand,
    country_summary,
    role_summary,
    company_summary,
    platform_summary,
    remote_summary,
    experience_summary,
):
    """
    Validate generated analytical datasets.
    """

    print("\n")
    print("=" * 70)
    print("FINAL ANALYTICAL DATA VALIDATION")
    print("=" * 70)

    datasets = {
        "job_postings_analysis": job_analysis,
        "skill_demand": skill_demand,
        "country_job_summary": country_summary,
        "role_summary": role_summary,
        "company_summary": company_summary,
        "platform_summary": platform_summary,
        "remote_summary": remote_summary,
        "experience_summary": experience_summary,
    }

    for name, df in datasets.items():

        print(
            f"\n{name}:"
        )

        print(
            f"  Rows: {len(df):,}"
        )

        print(
            f"  Columns: {len(df.columns)}"
        )

        print(
            f"  Missing values: "
            f"{df.isna().sum().sum():,}"
        )

        print(
            f"  Duplicate rows: "
            f"{df.duplicated().sum():,}"
        )

    print("\n")
    print("=" * 70)
    print("ANALYTICAL DATA PROCESSING COMPLETE")
    print("=" * 70)


# ============================================================
# 14. MAIN PIPELINE
# ============================================================

def main():

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    jobs, skills = load_data()

    # --------------------------------------------------------
    # Standardize
    # --------------------------------------------------------

    jobs, skills = standardize_data(
        jobs,
        skills
    )

    # --------------------------------------------------------
    # Build analytical datasets
    # --------------------------------------------------------

    job_analysis = build_job_analysis(
        jobs
    )

    skill_demand = build_skill_demand(
        skills,
        jobs
    )

    country_summary = build_country_summary(
        job_analysis
    )

    role_summary = build_role_summary(
        job_analysis
    )

    company_summary = build_company_summary(
        job_analysis
    )

    platform_summary = build_platform_summary(
        job_analysis
    )

    remote_summary = build_remote_summary(
        job_analysis
    )

    experience_summary = build_experience_summary(
        job_analysis
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("SAVING ANALYTICAL DATASETS")
    print("=" * 70)

    save_dataset(
        job_analysis,
        "job_postings_analysis.csv"
    )

    save_dataset(
        skill_demand,
        "skill_demand.csv"
    )

    save_dataset(
        country_summary,
        "country_job_summary.csv"
    )

    save_dataset(
        role_summary,
        "role_summary.csv"
    )

    save_dataset(
        company_summary,
        "company_summary.csv"
    )

    save_dataset(
        platform_summary,
        "platform_summary.csv"
    )

    save_dataset(
        remote_summary,
        "remote_summary.csv"
    )

    save_dataset(
        experience_summary,
        "experience_summary.csv"
    )

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    final_validation(
        job_analysis,
        skill_demand,
        country_summary,
        role_summary,
        company_summary,
        platform_summary,
        remote_summary,
        experience_summary,
    )


# ============================================================
# 15. RUN
# ============================================================

if __name__ == "__main__":
    main()