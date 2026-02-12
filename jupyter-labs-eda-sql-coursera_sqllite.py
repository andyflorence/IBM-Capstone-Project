"""
SpaceX SQL Analysis - EDA using SQLite
========================================

This script performs exploratory data analysis on SpaceX launch data using SQL queries.
The analysis covers launch sites, payload masses, landing outcomes, and mission success rates.

Original Notebook: jupyter-labs-eda-sql-coursera_sqllite.ipynb
Author: Lakshmi Holla
Contributors: Rav Ahuja
Converted to Python Script: 2026-02-10

Requirements:
- pandas
- sqlite3 (built-in)
- prettytable
"""

import sqlite3
import pandas as pd
from pathlib import Path
import sys

# Configuration
DATABASE_NAME = "my_data1.db"
TABLE_NAME = "SPACEXTBL"
DATA_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv"

# Set display options for better output
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def print_section_header(title):
    """Print a formatted section header."""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)


def execute_query(cursor, query, description=""):
    """
    Execute a SQL query and display results.
    
    Parameters:
    -----------
    cursor : sqlite3.Cursor
        Database cursor
    query : str
        SQL query to execute
    description : str
        Description of what the query does
    """
    if description:
        print(f"\n{description}")
        print("-" * 80)
    
    print(f"Query:\n{query}\n")
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Get column names
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            
            # Convert to DataFrame for better display
            df = pd.DataFrame(results, columns=columns)
            print(f"Results ({len(df)} rows):")
            print(df.to_string(index=False))
        else:
            print("Query executed successfully (no results to display)")
            
        return results
        
    except Exception as e:
        print(f"❌ Error executing query: {e}")
        return None


def main():
    """Main execution function."""
    
    print_section_header("SpaceX SQL Analysis - Exploratory Data Analysis")
    
    # ========================================================================
    # STEP 1: DATABASE SETUP
    # ========================================================================
    print_section_header("STEP 1: Database Setup and Data Loading")
    
    # Create database connection
    print("\n📊 Connecting to SQLite database...")
    con = sqlite3.connect(DATABASE_NAME)
    cur = con.cursor()
    print(f"✅ Connected to database: {DATABASE_NAME}")
    
    # Load data from CSV
    print(f"\n📥 Loading SpaceX data from URL...")
    try:
        df = pd.read_csv(DATA_URL)
        print(f"✅ Loaded {len(df)} records with {len(df.columns)} columns")
        
        # Display first few rows
        print("\nFirst 5 rows of data:")
        print(df.head().to_string())
        
        # Load into SQLite
        print(f"\n💾 Saving data to database table '{TABLE_NAME}'...")
        df.to_sql(TABLE_NAME, con, if_exists='replace', index=False, method="multi")
        print(f"✅ Data saved successfully")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        con.close()
        sys.exit(1)
    
    # ========================================================================
    # STEP 2: DATA CLEANING
    # ========================================================================
    print_section_header("STEP 2: Data Cleaning")
    
    # Drop SPACEXTABLE if it exists
    query_drop = "DROP TABLE IF EXISTS SPACEXTABLE;"
    execute_query(cur, query_drop, "Dropping SPACEXTABLE if it exists")
    con.commit()
    
    # Create clean table (remove null dates)
    query_create = "CREATE TABLE SPACEXTABLE AS SELECT * FROM SPACEXTBL WHERE Date IS NOT NULL"
    execute_query(cur, query_create, "Creating clean table (removing null dates)")
    con.commit()
    
    # ========================================================================
    # STEP 3: EXPLORATORY DATA ANALYSIS QUERIES
    # ========================================================================
    print_section_header("STEP 3: Exploratory Data Analysis")
    
    # Query 1: View table schema
    query_1 = "PRAGMA table_info(SPACEXTBL)"
    execute_query(cur, query_1, 
                  "Query 1: Display table schema (column names and types)")
    
    # Query 2: Distinct launch sites
    query_2 = """
    SELECT DISTINCT Launch_Site
    FROM SPACEXTBL;
    """
    execute_query(cur, query_2, 
                  "Query 2: Display unique launch sites")
    
    # Query 3: Launches from Cape Canaveral
    query_3 = """
    SELECT *
    FROM SPACEXTBL
    WHERE LAUNCH_SITE LIKE 'CCA%'
    LIMIT 5;
    """
    execute_query(cur, query_3, 
                  "Query 3: Display first 5 records with launch sites beginning with 'CCA'")
    
    # Query 4: Total payload mass for NASA (CRS)
    query_4 = """
    SELECT 
        SUM(PAYLOAD_MASS__KG_) AS TOTAL_PAYLOAD_MASS_KG
    FROM SPACEXTBL
    WHERE CUSTOMER = 'NASA (CRS)';
    """
    execute_query(cur, query_4, 
                  "Query 4: Total payload mass carried by NASA (CRS)")
    
    # Query 5: Average payload mass for F9 v1.1
    query_5 = """
    SELECT 
        AVG(PAYLOAD_MASS__KG_) AS AVG_PAYLOAD_MASS_KG
    FROM SPACEXTBL
    WHERE BOOSTER_VERSION = 'F9 v1.1';
    """
    execute_query(cur, query_5, 
                  "Query 5: Average payload mass for Booster Version 'F9 v1.1'")
    
    # Query 6: First successful ground pad landing
    query_6 = """
    SELECT 
        MIN(DATE) AS FIRST_SUCCESSFUL_GROUND_PAD_LANDING_DATE
    FROM SPACEXTBL
    WHERE LANDING_OUTCOME = 'Success (ground pad)';
    """
    execute_query(cur, query_6, 
                  "Query 6: Date of the first successful landing on a ground pad")
    
    # Query 7: Successful ground pad landings (detailed)
    query_7 = """
    SELECT DATE, Landing_Outcome 
    FROM SPACEXTBL
    WHERE Landing_Outcome = 'Success (ground pad)'
    ORDER BY Date ASC;
    """
    execute_query(cur, query_7, 
                  "Query 7: All successful ground pad landings (chronological order)")
    
    # Query 8: Distinct landing outcomes
    query_8 = """
    SELECT DISTINCT Landing_Outcome 
    FROM SPACEXTBL;
    """
    execute_query(cur, query_8, 
                  "Query 8: All distinct landing outcomes")
    
    # Query 9: Booster versions with specific criteria
    query_9 = """
    SELECT DISTINCT Booster_Version
    FROM SPACEXTBL
    WHERE Landing_Outcome = 'Success (drone ship)'
      AND PAYLOAD_MASS__KG_ > 4000
      AND PAYLOAD_MASS__KG_ < 6000;
    """
    execute_query(cur, query_9, 
                  "Query 9: Booster versions with successful drone ship landings (4000-6000 kg payload)")
    
    # Query 10: Distinct mission outcomes
    query_10 = """
    SELECT DISTINCT Mission_Outcome 
    FROM SPACEXTBL;
    """
    execute_query(cur, query_10, 
                  "Query 10: All distinct mission outcomes")
    
    # Query 11: Mission success vs failure count
    query_11 = """
    SELECT
        SUM(CASE 
                WHEN MISSION_OUTCOME LIKE '%Success%' THEN 1 
                ELSE 0 
            END) AS SUCCESSFUL_MISSIONS,
        SUM(CASE 
                WHEN MISSION_OUTCOME NOT LIKE '%Success%' THEN 1 
                ELSE 0 
            END) AS FAILED_MISSIONS
    FROM SPACEXTBL;
    """
    execute_query(cur, query_11, 
                  "Query 11: Count of successful vs failed missions")
    
    # Query 12: Booster version with maximum payload
    query_12 = """
    SELECT DISTINCT Booster_Version
    FROM SPACEXTBL
    WHERE PAYLOAD_MASS__KG_ = (
        SELECT MAX(PAYLOAD_MASS__KG_)
        FROM SPACEXTBL
    );
    """
    execute_query(cur, query_12, 
                  "Query 12: Booster version(s) that carried the maximum payload mass")
    
    # Query 13: Failed drone ship landings in 2015 (with month names)
    query_13 = """
    SELECT
        CASE substr(DATE, 6, 2)
            WHEN '01' THEN 'January'
            WHEN '02' THEN 'February'
            WHEN '03' THEN 'March'
            WHEN '04' THEN 'April'
            WHEN '05' THEN 'May'
            WHEN '06' THEN 'June'
            WHEN '07' THEN 'July'
            WHEN '08' THEN 'August'
            WHEN '09' THEN 'September'
            WHEN '10' THEN 'October'
            WHEN '11' THEN 'November'
            WHEN '12' THEN 'December'
        END AS MONTH_NAME,
        Landing_Outcome,
        Booster_Version,
        Launch_Site
    FROM SPACEXTBL
    WHERE substr(DATE, 0, 5) = '2015'
      AND Landing_Outcome LIKE 'Failure (drone ship)%';
    """
    execute_query(cur, query_13, 
                  "Query 13: Failed drone ship landings in 2015 (with month names)")
    
    # Query 14: Landing outcomes between specific dates
    query_14 = """
    SELECT
        LANDING_OUTCOME,
        COUNT(*) AS OUTCOME_COUNT
    FROM SPACEXTBL
    WHERE DATE BETWEEN '2010-06-04' AND '2017-03-20'
    GROUP BY LANDING_OUTCOME
    ORDER BY OUTCOME_COUNT DESC;
    """
    execute_query(cur, query_14, 
                  "Query 14: Landing outcome counts between 2010-06-04 and 2017-03-20")
    
    # ========================================================================
    # STEP 4: SUMMARY STATISTICS
    # ========================================================================
    print_section_header("STEP 4: Summary Statistics")
    
    # Overall statistics
    summary_query = """
    SELECT 
        COUNT(*) as TOTAL_LAUNCHES,
        COUNT(DISTINCT LAUNCH_SITE) as UNIQUE_LAUNCH_SITES,
        COUNT(DISTINCT BOOSTER_VERSION) as UNIQUE_BOOSTERS,
        MIN(DATE) as FIRST_LAUNCH,
        MAX(DATE) as LAST_LAUNCH,
        ROUND(AVG(PAYLOAD_MASS__KG_), 2) as AVG_PAYLOAD_KG,
        MAX(PAYLOAD_MASS__KG_) as MAX_PAYLOAD_KG
    FROM SPACEXTBL;
    """
    execute_query(cur, summary_query, 
                  "Overall Dataset Statistics")
    
    # ========================================================================
    # CLEANUP
    # ========================================================================
    print_section_header("Analysis Complete")
    
    print(f"\n💾 Database file: {DATABASE_NAME}")
    print(f"📊 Table name: {TABLE_NAME}")
    print("\n✅ All queries executed successfully!")
    
    # Close connection
    con.close()
    print("\n🔒 Database connection closed")
    
    print("\n" + "="*80)
    print("Thank you for using SpaceX SQL Analysis!")
    print("="*80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
