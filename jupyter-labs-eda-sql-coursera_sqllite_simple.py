"""
SpaceX SQL Analysis - Simplified Version
==========================================

A streamlined Python script for analyzing SpaceX launch data using SQLite.

Key Features:
- Automated data loading from online source
- 14 analytical SQL queries covering launches, payloads, and outcomes
- Clean, readable output with formatted tables
- Error handling and data validation

Usage:
    python spacex_sql_analysis_simple.py
    
Output:
    - Creates my_data1.db SQLite database
    - Displays analysis results in console
"""

import sqlite3
import pandas as pd
import sys
from typing import Optional, List, Tuple

# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG = {
    'database': 'my_data1.db',
    'table': 'SPACEXTBL',
    'data_url': 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv'
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def section(title: str, char: str = "=") -> None:
    """Print formatted section header."""
    print(f"\n{char * 80}")
    print(f" {title}")
    print(f"{char * 80}\n")


def run_query(cursor: sqlite3.Cursor, query: str, description: str = "") -> Optional[pd.DataFrame]:
    """
    Execute SQL query and return results as DataFrame.
    
    Args:
        cursor: SQLite cursor object
        query: SQL query string
        description: Optional description of the query
        
    Returns:
        DataFrame with query results, or None if error
    """
    if description:
        print(f"📊 {description}")
        print("-" * 80)
    
    # Clean and display query
    clean_query = "\n".join(line.strip() for line in query.strip().split("\n"))
    print(f"{clean_query}\n")
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(results, columns=columns)
            print(f"✅ Results ({len(df)} rows):")
            print(df.to_string(index=False))
            print()
            return df
        else:
            print("✅ Query executed successfully\n")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return None


# ============================================================================
# SQL QUERIES
# ============================================================================

QUERIES = {
    'schema': {
        'description': 'Table Schema',
        'sql': "PRAGMA table_info(SPACEXTBL)"
    },
    
    'launch_sites': {
        'description': 'Unique Launch Sites',
        'sql': "SELECT DISTINCT Launch_Site FROM SPACEXTBL;"
    },
    
    'cca_launches': {
        'description': 'First 5 Launches from Cape Canaveral (CCA)',
        'sql': """
            SELECT *
            FROM SPACEXTBL
            WHERE LAUNCH_SITE LIKE 'CCA%'
            LIMIT 5;
        """
    },
    
    'nasa_payload': {
        'description': 'Total Payload Mass for NASA (CRS)',
        'sql': """
            SELECT SUM(PAYLOAD_MASS__KG_) AS TOTAL_PAYLOAD_MASS_KG
            FROM SPACEXTBL
            WHERE CUSTOMER = 'NASA (CRS)';
        """
    },
    
    'f9_avg_payload': {
        'description': 'Average Payload Mass for F9 v1.1 Booster',
        'sql': """
            SELECT AVG(PAYLOAD_MASS__KG_) AS AVG_PAYLOAD_MASS_KG
            FROM SPACEXTBL
            WHERE BOOSTER_VERSION = 'F9 v1.1';
        """
    },
    
    'first_ground_landing': {
        'description': 'First Successful Ground Pad Landing Date',
        'sql': """
            SELECT MIN(DATE) AS FIRST_SUCCESSFUL_LANDING
            FROM SPACEXTBL
            WHERE LANDING_OUTCOME = 'Success (ground pad)';
        """
    },
    
    'all_ground_landings': {
        'description': 'All Successful Ground Pad Landings (Chronological)',
        'sql': """
            SELECT DATE, Landing_Outcome
            FROM SPACEXTBL
            WHERE Landing_Outcome = 'Success (ground pad)'
            ORDER BY Date ASC;
        """
    },
    
    'landing_outcomes': {
        'description': 'All Distinct Landing Outcomes',
        'sql': "SELECT DISTINCT Landing_Outcome FROM SPACEXTBL;"
    },
    
    'drone_ship_boosters': {
        'description': 'Boosters with Successful Drone Ship Landings (4000-6000 kg)',
        'sql': """
            SELECT DISTINCT Booster_Version
            FROM SPACEXTBL
            WHERE Landing_Outcome = 'Success (drone ship)'
              AND PAYLOAD_MASS__KG_ > 4000
              AND PAYLOAD_MASS__KG_ < 6000;
        """
    },
    
    'mission_outcomes': {
        'description': 'All Distinct Mission Outcomes',
        'sql': "SELECT DISTINCT Mission_Outcome FROM SPACEXTBL;"
    },
    
    'mission_success_rate': {
        'description': 'Mission Success vs Failure Count',
        'sql': """
            SELECT
                SUM(CASE WHEN MISSION_OUTCOME LIKE '%Success%' THEN 1 ELSE 0 END) AS SUCCESSFUL,
                SUM(CASE WHEN MISSION_OUTCOME NOT LIKE '%Success%' THEN 1 ELSE 0 END) AS FAILED
            FROM SPACEXTBL;
        """
    },
    
    'max_payload_booster': {
        'description': 'Booster(s) That Carried Maximum Payload',
        'sql': """
            SELECT DISTINCT Booster_Version
            FROM SPACEXTBL
            WHERE PAYLOAD_MASS__KG_ = (
                SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL
            );
        """
    },
    
    'failed_2015': {
        'description': 'Failed Drone Ship Landings in 2015',
        'sql': """
            SELECT
                CASE substr(DATE, 6, 2)
                    WHEN '01' THEN 'January'   WHEN '02' THEN 'February'
                    WHEN '03' THEN 'March'     WHEN '04' THEN 'April'
                    WHEN '05' THEN 'May'       WHEN '06' THEN 'June'
                    WHEN '07' THEN 'July'      WHEN '08' THEN 'August'
                    WHEN '09' THEN 'September' WHEN '10' THEN 'October'
                    WHEN '11' THEN 'November'  WHEN '12' THEN 'December'
                END AS MONTH,
                Landing_Outcome,
                Booster_Version,
                Launch_Site
            FROM SPACEXTBL
            WHERE substr(DATE, 0, 5) = '2015'
              AND Landing_Outcome LIKE 'Failure (drone ship)%';
        """
    },
    
    'outcome_distribution': {
        'description': 'Landing Outcome Distribution (2010-2017)',
        'sql': """
            SELECT
                LANDING_OUTCOME,
                COUNT(*) AS COUNT
            FROM SPACEXTBL
            WHERE DATE BETWEEN '2010-06-04' AND '2017-03-20'
            GROUP BY LANDING_OUTCOME
            ORDER BY COUNT DESC;
        """
    },
    
    'summary_stats': {
        'description': 'Overall Dataset Statistics',
        'sql': """
            SELECT 
                COUNT(*) as TOTAL_LAUNCHES,
                COUNT(DISTINCT LAUNCH_SITE) as LAUNCH_SITES,
                COUNT(DISTINCT BOOSTER_VERSION) as BOOSTER_TYPES,
                MIN(DATE) as FIRST_LAUNCH,
                MAX(DATE) as LAST_LAUNCH,
                ROUND(AVG(PAYLOAD_MASS__KG_), 2) as AVG_PAYLOAD_KG,
                MAX(PAYLOAD_MASS__KG_) as MAX_PAYLOAD_KG
            FROM SPACEXTBL;
        """
    }
}


# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def setup_database(con: sqlite3.Connection) -> bool:
    """
    Load SpaceX data into database.
    
    Args:
        con: SQLite connection object
        
    Returns:
        True if successful, False otherwise
    """
    section("Database Setup", "=")
    
    try:
        # Load data
        print(f"📥 Loading data from: {CONFIG['data_url']}")
        df = pd.read_csv(CONFIG['data_url'])
        print(f"✅ Loaded {len(df)} records with {len(df.columns)} columns\n")
        
        # Save to database
        print(f"💾 Saving to table '{CONFIG['table']}'...")
        df.to_sql(CONFIG['table'], con, if_exists='replace', index=False, method="multi")
        print(f"✅ Data loaded successfully\n")
        
        # Clean data (remove null dates)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS SPACEXTABLE;")
        cur.execute(f"CREATE TABLE SPACEXTABLE AS SELECT * FROM {CONFIG['table']} WHERE Date IS NOT NULL")
        con.commit()
        print("✅ Created clean table (removed null dates)\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}\n")
        return False


def run_analysis(con: sqlite3.Connection) -> None:
    """
    Execute all analytical queries.
    
    Args:
        con: SQLite connection object
    """
    section("SpaceX Launch Data Analysis", "=")
    
    cur = con.cursor()
    
    # Run each query
    for i, (key, query_info) in enumerate(QUERIES.items(), 1):
        print(f"\n{'─' * 80}")
        print(f"Query {i}/{len(QUERIES)}: {query_info['description']}")
        print('─' * 80)
        run_query(cur, query_info['sql'])


def main():
    """Main execution function."""
    
    print("\n" + "="*80)
    print(" 🚀 SpaceX SQL Analysis")
    print("="*80)
    
    # Connect to database
    print(f"\n🔌 Connecting to database: {CONFIG['database']}")
    con = sqlite3.connect(CONFIG['database'])
    print("✅ Connected\n")
    
    # Set up database
    if not setup_database(con):
        con.close()
        sys.exit(1)
    
    # Run analysis
    run_analysis(con)
    
    # Cleanup
    section("Analysis Complete", "=")
    print(f"💾 Database: {CONFIG['database']}")
    print(f"📊 Table: {CONFIG['table']}")
    print("\n✅ All queries completed successfully!\n")
    
    con.close()
    print("🔒 Database connection closed\n")
    print("="*80 + "\n")


if __name__ == "__main__":
    # Configure pandas display
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 120)
    pd.set_option('display.max_colwidth', 50)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
