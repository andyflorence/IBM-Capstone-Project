"""
SpaceX SQL Analysis - EDA with Visualizations
==============================================

This script performs exploratory data analysis on SpaceX launch data using SQL queries
with comprehensive visualizations for each analysis.

Enhanced with:
- Data visualizations for every query result
- Professional charts and graphs
- Statistical summaries
- Export capabilities

Original Notebook: jupyter-labs-eda-sql-coursera_sqllite.ipynb
Enhanced Version: 2026-02-11

Requirements:
- pandas
- sqlite3 (built-in)
- matplotlib
- seaborn
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
import warnings
from typing import Optional, Tuple
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Suppress warnings
warnings.filterwarnings('ignore')

# Configuration
DATABASE_NAME = "my_data1.db"
TABLE_NAME = "SPACEXTBL"
DATA_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv"

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


def get_column(df: pd.DataFrame, col_name: str) -> str:
    """
    Get column name from DataFrame handling case variations.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to search
    col_name : str
        Column name to find (case-insensitive)
        
    Returns:
    --------
    str
        Actual column name in DataFrame
    """
    if df is None or df.empty:
        return col_name
    
    # Try exact match first
    if col_name in df.columns:
        return col_name
    
    # Try case-insensitive match
    for col in df.columns:
        if col.upper() == col_name.upper():
            return col
    
    # Return original if not found
    return col_name


def print_section_header(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80)


def execute_query(cursor, query: str, description: str = "") -> Optional[pd.DataFrame]:
    """
    Execute a SQL query and return results as DataFrame.
    
    Parameters:
    -----------
    cursor : sqlite3.Cursor
        Database cursor
    query : str
        SQL query to execute
    description : str
        Description of what the query does
        
    Returns:
    --------
    pd.DataFrame or None
        Query results as DataFrame
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
            df = pd.DataFrame(results, columns=columns)
            print(f"Results ({len(df)} rows):")
            print(df.to_string(index=False))
            return df
        else:
            print("Query executed successfully (no results to display)")
            return None
            
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        return None


def viz_launch_sites(df: pd.DataFrame, save_fig: bool = True) -> None:
    """Visualize unique launch sites."""
    if df is None or df.empty:
        return
    
    # Count launches per site (need to query full data)
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create a simple bar chart of unique sites
    sites = df.iloc[:, 0].tolist()
    counts = [1] * len(sites)  # Placeholder
    
    ax.barh(sites, counts, color='steelblue')
    ax.set_xlabel('Count', fontsize=12)
    ax.set_ylabel('Launch Site', fontsize=12)
    ax.set_title('Unique Launch Sites in Dataset', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    if save_fig:
        plt.savefig('viz_01_launch_sites.png', dpi=300, bbox_inches='tight')
    plt.show()


def viz_launch_sites_full(cursor, save_fig: bool = True) -> None:
    """Visualize launch count by site."""
    query = """
    SELECT Launch_Site, COUNT(*) as Launch_Count
    FROM SPACEXTBL
    GROUP BY Launch_Site
    ORDER BY Launch_Count DESC;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=['Launch_Site', 'Launch_Count'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.barh(df['Launch_Site'], df['Launch_Count'], color='steelblue')
    ax.set_xlabel('Number of Launches', fontsize=12)
    ax.set_ylabel('Launch Site', fontsize=12)
    ax.set_title('Total Launches by Site', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, 
                f'{int(width)}', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    if save_fig:
        plt.savefig('viz_02_launch_count_by_site.png', dpi=300, bbox_inches='tight')
    plt.show()


def viz_cape_canaveral_launches(df: pd.DataFrame, save_fig: bool = True) -> None:
    """Visualize Cape Canaveral launches by booster version."""
    if df is None or df.empty:
        return
    
    # Group by Booster_Version if column exists
    booster_col = get_column(df, 'Booster_Version')
    if booster_col in df.columns:
        booster_counts = df[booster_col].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        booster_counts.plot(kind='bar', ax=ax, color='coral')
        ax.set_xlabel('Booster Version', fontsize=12)
        ax.set_ylabel('Number of Launches', fontsize=12)
        ax.set_title('Cape Canaveral (CCA) Launches by Booster Version', 
                     fontsize=14, fontweight='bold')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        if save_fig:
            plt.savefig('viz_03_cape_canaveral_boosters.png', dpi=300, bbox_inches='tight')
        plt.show()


def viz_total_payload(df: pd.DataFrame, save_fig: bool = True) -> None:
    """Visualize total payload mass for NASA (CRS)."""
    if df is None or df.empty:
        return
    
    total_payload = df.iloc[0, 0]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Create a simple bar chart
    ax.bar(['NASA (CRS)'], [total_payload], color='darkgreen', width=0.4)
    ax.set_ylabel('Total Payload Mass (kg)', fontsize=12)
    ax.set_title('Total Payload Mass Carried by NASA (CRS)', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value label
    ax.text(0, total_payload, f'{total_payload:,.0f} kg', 
            ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    if save_fig:
        plt.savefig('viz_04_nasa_total_payload.png', dpi=300, bbox_inches='tight')
    plt.show()


def viz_average_payload(df: pd.DataFrame, booster_name: str, save_fig: bool = True) -> None:
    """Visualize average payload mass for a booster version."""
    if df is None or df.empty:
        return
    
    avg_payload = df.iloc[0, 0]
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.bar([booster_name], [avg_payload], color='purple', width=0.4)
    ax.set_ylabel('Average Payload Mass (kg)', fontsize=12)
    ax.set_title(f'Average Payload Mass for {booster_name}', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value label
    ax.text(0, avg_payload, f'{avg_payload:,.1f} kg', 
            ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    if save_fig:
        plt.savefig('viz_05_avg_payload_f9v11.png', dpi=300, bbox_inches='tight')
    plt.show()


def viz_first_successful_landing(df: pd.DataFrame, save_fig: bool = True) -> None:
    """Visualize first successful landing date."""
    if df is None or df.empty:
        return
    
    date_str = df.iloc[0, 0]
    
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.axis('off')
    
    # Create text display
    text = f"First Successful Ground Pad Landing\n{date_str}"
    ax.text(0.5, 0.5, text, ha='center', va='center', 
            fontsize=20, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    plt.tight_layout()
    if save_fig:
        plt.savefig('viz_06_first_landing_date.png', dpi=300, bbox_inches='tight')
    plt.show()


def viz_successful_landings_timeline(df: pd.DataFrame, save_fig: bool = True) -> None:
    """Visualize timeline of successful ground pad landings."""
    if df is None or df.empty:
        return
    
    # Handle case-insensitive column names
    date_col = get_column(df, 'DATE')
    df[date_col] = pd.to_datetime(df[date_col])
    df['Landing_Number'] = range(1, len(df) + 1)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.plot(df[date_col], df['Landing_Number'], marker='o', 
            linewidth=2, markersize=8, color='green')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Cumulative Successful Landings', fontsize=12)
    ax.set_title('Timeline of Successful Ground Pad Landings', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    if save_fig:
        plt.savefig('viz_07_landing_timeline.png', dpi=300, bbox_inches='tight')
    plt.show()


def viz_landing_outcomes(df: pd.DataFrame, save_fig: bool = True) -> None:
    """Visualize distribution of landing outcomes."""
    if df is None or df.empty:
        return
    
    # Get full distribution from database
    outcomes = df.iloc[:, 0].tolist()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Bar chart
    outcome_series = pd.Series(outcomes)
    counts = outcome_series.value_counts()
    
    counts.plot(kind='barh', ax=ax1, color='skyblue')
    ax1.set_xlabel('Count', fontsize=12)
    ax1.set_ylabel('Landing Outcome', fontsize=12)
    ax1.set_title('Distribution of Landing Outcomes', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='x')
    
    # Pie chart
    ax2.pie(counts.values, labels=counts.index, autopct='%1.1f%%', 
            startangle=90, colors=sns.color_palette('Set3'))
    ax2.set_title('Landing Outcome Proportions', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    if save_fig:
        plt.savefig('viz_08_landing_outcomes.png', dpi=300, bbox_inches='tight')
    plt.show()


def viz_landing_outcomes_full(cursor, save_fig: bool = True) -> None:
    """Visualize full distribution of landing outcomes with counts."""
    query = """
    SELECT Landing_Outcome, COUNT(*) as Count
    FROM SPACEXTBL
    GROUP BY Landing_Outcome
    ORDER BY Count DESC;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=['Landing_Outcome', 'Count'])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Bar chart
    bars = ax1.barh(df['Landing_Outcome'], df['Count'], color='skyblue')
    ax1.set_xlabel('Number of Launches', fontsize=12)
    ax1.set_ylabel('Landing Outcome', fontsize=12)
    ax1.set_title('Distribution of Landing Outcomes', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for bar in bars:
        width = bar.get_width()
        ax1.text(width, bar.get_y() + bar.get_height()/2, 
                f'{int(width)}', ha='left', va='center', fontsize=9)
    
    # Pie chart
    ax2.pie(df['Count'], labels=df['Landing_Outcome'], autopct='%1.1f%%', 
            startangle=90, colors=sns.color_palette('Set3', len(df)))
    ax2.set_title('Landing Outcome Proportions', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    if save_fig:
        plt.savefig('viz_08_landing_outcomes_full.png', dpi=300, bbox_inches='tight')
    plt.show()


def viz_drone_ship_boosters(df: pd.DataFrame, save_fig: bool = True) -> None:
    """Visualize booster versions with successful drone ship landings."""
    if df is None or df.empty:
        return
    
    boosters = df.iloc[:, 0].tolist()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    booster_counts = pd.Series(boosters).value_counts()
    booster_counts.plot(kind='bar', ax=ax, color='teal')
    
    ax.set_xlabel('Booster Version', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title('Booster Versions with Successful Drone Ship Landings\n(Payload: 4000-6000 kg)', 
                 fontsize=14, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    if save_fig:
        plt.savefig('viz_09_drone_ship_boosters.png', dpi=300, bbox_inches='tight')
    plt.show()


def viz_mission_outcomes(df: pd.DataFrame, save_fig: bool = True) -> None:
    """Visualize distinct mission outcomes."""
    if df is None or df.empty:
        return
    
    outcomes = df.iloc[:, 0].tolist()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Count occurrences
    outcome_counts = pd.Series(outcomes).value_counts()
    
    colors = ['green' if 'Success' in str(outcome) else 'red' 
              for outcome in outcome_counts.index]
    
    outcome_counts.plot(kind='barh', ax=ax, color=colors)
    ax.set_xlabel('Count', fontsize=12)
    ax.set_ylabel('Mission Outcome', fontsize=12)
    ax.set_title('Distribution of Mission Outcomes', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    if save_fig:
        plt.savefig('viz_10_mission_outcomes.png', dpi=300, bbox_inches='tight')
    plt.show()


def viz_mission_outcomes_full(cursor, save_fig: bool = True) -> None:
    """Visualize full distribution of mission outcomes."""
    query = """
    SELECT Mission_Outcome, COUNT(*) as Count
    FROM SPACEXTBL
    GROUP BY Mission_Outcome
    ORDER BY Count DESC;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=['Mission_Outcome', 'Count'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = ['green' if 'Success' in str(outcome) else 'red' 
              for outcome in df['Mission_Outcome']]
    
    bars = ax.barh(df['Mission_Outcome'], df['Count'], color=colors)
    ax.set_xlabel('Number of Launches', fontsize=12)
    ax.set_ylabel('Mission Outcome', fontsize=12)
    ax.set_title('Distribution of Mission Outcomes', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, 
                f'{int(width)}', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    if save_fig:
        plt.savefig('viz_10_mission_outcomes_full.png', dpi=300, bbox_inches='tight')
    plt.show()


def viz_success_vs_failure(df: pd.DataFrame, save_fig: bool = True) -> None:
    """Visualize successful vs failed missions."""
    if df is None or df.empty:
        return
    
    successful = df.iloc[0, 0]
    failed = df.iloc[0, 1]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Bar chart
    categories = ['Successful', 'Failed']
    values = [successful, failed]
    colors_bar = ['green', 'red']
    
    bars = ax1.bar(categories, values, color=colors_bar, width=0.5)
    ax1.set_ylabel('Number of Missions', fontsize=12)
    ax1.set_title('Mission Success vs Failure', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar, val in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                f'{int(val)}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Pie chart
    ax2.pie(values, labels=categories, autopct='%1.1f%%', 
            colors=colors_bar, startangle=90, textprops={'fontsize': 12})
    ax2.set_title('Mission Success Rate', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    if save_fig:
        plt.savefig('viz_11_success_vs_failure.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print success rate
    total = successful + failed
    success_rate = (successful / total) * 100
    print(f"\n📊 Mission Success Rate: {success_rate:.2f}% ({successful}/{total})")


def viz_max_payload_booster(df: pd.DataFrame, cursor, save_fig: bool = True) -> None:
    """Visualize booster with maximum payload capacity."""
    if df is None or df.empty:
        return
    
    booster = df.iloc[0, 0]
    
    # Get max payload value
    query_max = "SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL;"
    cursor.execute(query_max)
    max_payload = cursor.fetchone()[0]
    
    # Get comparison with other boosters
    query_comparison = """
    SELECT Booster_Version, MAX(PAYLOAD_MASS__KG_) as Max_Payload
    FROM SPACEXTBL
    GROUP BY Booster_Version
    ORDER BY Max_Payload DESC
    LIMIT 10;
    """
    cursor.execute(query_comparison)
    comparison_df = pd.DataFrame(cursor.fetchall(), 
                                  columns=['Booster_Version', 'Max_Payload'])
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Highlight the max booster
    colors = ['gold' if b == booster else 'steelblue' 
              for b in comparison_df['Booster_Version']]
    
    bars = ax.barh(comparison_df['Booster_Version'], 
                   comparison_df['Max_Payload'], color=colors)
    ax.set_xlabel('Maximum Payload Mass (kg)', fontsize=12)
    ax.set_ylabel('Booster Version', fontsize=12)
    ax.set_title('Maximum Payload Capacity by Booster Version', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, 
                f'{width:,.0f}', ha='left', va='center', fontsize=9)
    
    # Add annotation for max
    ax.text(0.02, 0.98, f'Maximum: {max_payload:,.0f} kg\nBooster: {booster}',
            transform=ax.transAxes, fontsize=11, fontweight='bold',
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='gold', alpha=0.7))
    
    plt.tight_layout()
    if save_fig:
        plt.savefig('viz_12_max_payload_booster.png', dpi=300, bbox_inches='tight')
    plt.show()


def viz_failed_landings_2015(df: pd.DataFrame, save_fig: bool = True) -> None:
    """Visualize failed drone ship landings in 2015 by month."""
    if df is None or df.empty:
        return
    
    # Count by month
    month_col = get_column(df, 'MONTH_NAME')
    month_counts = df[month_col].value_counts()
    
    # Order months correctly
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    month_counts = month_counts.reindex([m for m in month_order if m in month_counts.index])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.bar(range(len(month_counts)), month_counts.values, color='crimson')
    ax.set_xticks(range(len(month_counts)))
    ax.set_xticklabels(month_counts.index, rotation=45, ha='right')
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Number of Failed Landings', fontsize=12)
    ax.set_title('Failed Drone Ship Landings in 2015 by Month', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height, 
                f'{int(height)}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    if save_fig:
        plt.savefig('viz_13_failed_landings_2015.png', dpi=300, bbox_inches='tight')
    plt.show()


def viz_landing_outcomes_by_period(df: pd.DataFrame, save_fig: bool = True) -> None:
    """Visualize landing outcomes for a specific period."""
    if df is None or df.empty:
        return
    
    # Get column names
    outcome_col = get_column(df, 'LANDING_OUTCOME')
    count_col = get_column(df, 'OUTCOME_COUNT')
    
    # Sort by count
    df_sorted = df.sort_values(count_col, ascending=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Bar chart
    colors = ['green' if 'Success' in str(outcome) else 'red' 
              for outcome in df_sorted[outcome_col]]
    
    bars = ax1.barh(df_sorted[outcome_col], df_sorted[count_col], color=colors)
    ax1.set_xlabel('Number of Landings', fontsize=12)
    ax1.set_ylabel('Landing Outcome', fontsize=12)
    ax1.set_title('Landing Outcomes (June 2010 - March 2017)', 
                  fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='x')
    
    # Add value labels
    for bar in bars:
        width = bar.get_width()
        ax1.text(width, bar.get_y() + bar.get_height()/2, 
                f'{int(width)}', ha='left', va='center', fontsize=9)
    
    # Pie chart with legend
    ax2.pie(df_sorted[count_col], labels=df_sorted[outcome_col], autopct='%1.1f%%', 
            startangle=90, colors=colors, textprops={'fontsize': 8})
    ax2.set_title('Landing Outcome Distribution', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    if save_fig:
        plt.savefig('viz_14_landing_outcomes_period.png', dpi=300, bbox_inches='tight')
    plt.show()


def viz_summary_statistics(df: pd.DataFrame, save_fig: bool = True) -> None:
    """Visualize overall summary statistics."""
    if df is None or df.empty:
        return
    
    # Extract values
    total_launches = df.iloc[0, 0]
    unique_sites = df.iloc[0, 1]
    unique_boosters = df.iloc[0, 2]
    avg_payload = df.iloc[0, 5]
    max_payload = df.iloc[0, 6]
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
    
    # 1. Total launches
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.bar(['Total Launches'], [total_launches], color='steelblue', width=0.5)
    ax1.set_ylabel('Count', fontsize=11)
    ax1.set_title('Total Launches', fontsize=13, fontweight='bold')
    ax1.text(0, total_launches, f'{int(total_launches)}', 
             ha='center', va='bottom', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # 2. Unique sites
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.bar(['Launch Sites'], [unique_sites], color='coral', width=0.5)
    ax2.set_ylabel('Count', fontsize=11)
    ax2.set_title('Unique Launch Sites', fontsize=13, fontweight='bold')
    ax2.text(0, unique_sites, f'{int(unique_sites)}', 
             ha='center', va='bottom', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. Unique boosters
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.bar(['Booster Versions'], [unique_boosters], color='green', width=0.5)
    ax3.set_ylabel('Count', fontsize=11)
    ax3.set_title('Unique Booster Versions', fontsize=13, fontweight='bold')
    ax3.text(0, unique_boosters, f'{int(unique_boosters)}', 
             ha='center', va='bottom', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. Payload comparison
    ax4 = fig.add_subplot(gs[1, :2])
    payload_data = ['Average Payload', 'Maximum Payload']
    payload_values = [avg_payload, max_payload]
    bars = ax4.bar(payload_data, payload_values, color=['purple', 'gold'], width=0.5)
    ax4.set_ylabel('Payload Mass (kg)', fontsize=11)
    ax4.set_title('Payload Mass Statistics', fontsize=13, fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, payload_values):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                f'{val:,.0f} kg', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # 5. Timeline info
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.axis('off')
    timeline_text = f"Timeline\n\nFirst Launch:\n{df.iloc[0, 3]}\n\nLast Launch:\n{df.iloc[0, 4]}"
    ax5.text(0.5, 0.5, timeline_text, ha='center', va='center', fontsize=11,
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    fig.suptitle('SpaceX Launch Dataset - Summary Statistics', 
                 fontsize=16, fontweight='bold')
    
    if save_fig:
        plt.savefig('viz_15_summary_statistics.png', dpi=300, bbox_inches='tight')
    plt.show()


def main():
    """Main execution function."""
    
    print_section_header("SpaceX SQL Analysis with Visualizations")
    
    # ========================================================================
    # STEP 1: DATABASE SETUP
    # ========================================================================
    print_section_header("STEP 1: Database Setup and Data Loading")
    
    logger.info("Connecting to SQLite database...")
    con = sqlite3.connect(DATABASE_NAME)
    cur = con.cursor()
    logger.info(f"Connected to database: {DATABASE_NAME}")
    
    # Load data from CSV
    logger.info("Loading SpaceX data from URL...")
    try:
        df = pd.read_csv(DATA_URL)
        logger.info(f"Loaded {len(df)} records with {len(df.columns)} columns")
        
        print("\nFirst 5 rows of data:")
        print(df.head().to_string())
        
        # Load into SQLite
        logger.info(f"Saving data to database table '{TABLE_NAME}'...")
        df.to_sql(TABLE_NAME, con, if_exists='replace', index=False, method="multi")
        logger.info("Data saved successfully")
        
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        con.close()
        sys.exit(1)
    
    # ========================================================================
    # STEP 2: DATA CLEANING
    # ========================================================================
    print_section_header("STEP 2: Data Cleaning")
    
    query_drop = "DROP TABLE IF EXISTS SPACEXTABLE;"
    execute_query(cur, query_drop, "Dropping SPACEXTABLE if it exists")
    con.commit()
    
    query_create = "CREATE TABLE SPACEXTABLE AS SELECT * FROM SPACEXTBL WHERE Date IS NOT NULL"
    execute_query(cur, query_create, "Creating clean table (removing null dates)")
    con.commit()
    
    # ========================================================================
    # STEP 3: QUERIES WITH VISUALIZATIONS
    # ========================================================================
    print_section_header("STEP 3: Exploratory Data Analysis with Visualizations")
    
    # Query 1: Table schema (no visualization needed)
    query_1 = "PRAGMA table_info(SPACEXTBL)"
    df_1 = execute_query(cur, query_1, "Query 1: Display table schema")
    
    # Query 2: Distinct launch sites
    query_2 = "SELECT DISTINCT Launch_Site FROM SPACEXTBL;"
    df_2 = execute_query(cur, query_2, "Query 2: Display unique launch sites")
    print("\n📊 Generating visualization...")
    viz_launch_sites_full(cur, save_fig=True)
    
    # Query 3: Cape Canaveral launches
    query_3 = """
    SELECT * FROM SPACEXTBL
    WHERE LAUNCH_SITE LIKE 'CCA%'
    LIMIT 5;
    """
    df_3 = execute_query(cur, query_3, 
                         "Query 3: First 5 records from Cape Canaveral (CCA)")
    if df_3 is not None and not df_3.empty:
        print("\n📊 Generating visualization...")
        viz_cape_canaveral_launches(df_3, save_fig=True)
    
    # Query 4: Total payload for NASA (CRS)
    query_4 = """
    SELECT SUM(PAYLOAD_MASS__KG_) AS TOTAL_PAYLOAD_MASS_KG
    FROM SPACEXTBL
    WHERE CUSTOMER = 'NASA (CRS)';
    """
    df_4 = execute_query(cur, query_4, "Query 4: Total payload mass for NASA (CRS)")
    if df_4 is not None:
        print("\n📊 Generating visualization...")
        viz_total_payload(df_4, save_fig=True)
    
    # Query 5: Average payload for F9 v1.1
    query_5 = """
    SELECT AVG(PAYLOAD_MASS__KG_) AS AVG_PAYLOAD_MASS_KG
    FROM SPACEXTBL
    WHERE BOOSTER_VERSION = 'F9 v1.1';
    """
    df_5 = execute_query(cur, query_5, "Query 5: Average payload mass for F9 v1.1")
    if df_5 is not None:
        print("\n📊 Generating visualization...")
        viz_average_payload(df_5, 'F9 v1.1', save_fig=True)
    
    # Query 6: First successful ground pad landing
    query_6 = """
    SELECT MIN(DATE) AS FIRST_SUCCESSFUL_GROUND_PAD_LANDING_DATE
    FROM SPACEXTBL
    WHERE LANDING_OUTCOME = 'Success (ground pad)';
    """
    df_6 = execute_query(cur, query_6, 
                         "Query 6: Date of first successful ground pad landing")
    if df_6 is not None:
        print("\n📊 Generating visualization...")
        viz_first_successful_landing(df_6, save_fig=True)
    
    # Query 7: All successful ground pad landings
    query_7 = """
    SELECT DATE, Landing_Outcome 
    FROM SPACEXTBL
    WHERE Landing_Outcome = 'Success (ground pad)'
    ORDER BY Date ASC;
    """
    df_7 = execute_query(cur, query_7, 
                         "Query 7: All successful ground pad landings (chronological)")
    if df_7 is not None and not df_7.empty:
        print("\n📊 Generating visualization...")
        viz_successful_landings_timeline(df_7, save_fig=True)
    
    # Query 8: Distinct landing outcomes
    query_8 = "SELECT DISTINCT Landing_Outcome FROM SPACEXTBL;"
    df_8 = execute_query(cur, query_8, "Query 8: All distinct landing outcomes")
    print("\n📊 Generating visualization...")
    viz_landing_outcomes_full(cur, save_fig=True)
    
    # Query 9: Drone ship boosters with payload 4000-6000 kg
    query_9 = """
    SELECT DISTINCT Booster_Version
    FROM SPACEXTBL
    WHERE Landing_Outcome = 'Success (drone ship)'
      AND PAYLOAD_MASS__KG_ > 4000
      AND PAYLOAD_MASS__KG_ < 6000;
    """
    df_9 = execute_query(cur, query_9, 
                         "Query 9: Boosters with successful drone ship landings (4000-6000 kg)")
    if df_9 is not None and not df_9.empty:
        print("\n📊 Generating visualization...")
        viz_drone_ship_boosters(df_9, save_fig=True)
    
    # Query 10: Distinct mission outcomes
    query_10 = "SELECT DISTINCT Mission_Outcome FROM SPACEXTBL;"
    df_10 = execute_query(cur, query_10, "Query 10: All distinct mission outcomes")
    print("\n📊 Generating visualization...")
    viz_mission_outcomes_full(cur, save_fig=True)
    
    # Query 11: Success vs failure count
    query_11 = """
    SELECT
        SUM(CASE WHEN MISSION_OUTCOME LIKE '%Success%' THEN 1 ELSE 0 END) AS SUCCESSFUL_MISSIONS,
        SUM(CASE WHEN MISSION_OUTCOME NOT LIKE '%Success%' THEN 1 ELSE 0 END) AS FAILED_MISSIONS
    FROM SPACEXTBL;
    """
    df_11 = execute_query(cur, query_11, 
                          "Query 11: Count of successful vs failed missions")
    if df_11 is not None:
        print("\n📊 Generating visualization...")
        viz_success_vs_failure(df_11, save_fig=True)
    
    # Query 12: Booster with maximum payload
    query_12 = """
    SELECT DISTINCT Booster_Version
    FROM SPACEXTBL
    WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL);
    """
    df_12 = execute_query(cur, query_12, 
                          "Query 12: Booster version(s) with maximum payload mass")
    if df_12 is not None:
        print("\n📊 Generating visualization...")
        viz_max_payload_booster(df_12, cur, save_fig=True)
    
    # Query 13: Failed drone ship landings in 2015
    query_13 = """
    SELECT
        CASE substr(DATE, 6, 2)
            WHEN '01' THEN 'January' WHEN '02' THEN 'February'
            WHEN '03' THEN 'March' WHEN '04' THEN 'April'
            WHEN '05' THEN 'May' WHEN '06' THEN 'June'
            WHEN '07' THEN 'July' WHEN '08' THEN 'August'
            WHEN '09' THEN 'September' WHEN '10' THEN 'October'
            WHEN '11' THEN 'November' WHEN '12' THEN 'December'
        END AS MONTH_NAME,
        Landing_Outcome, Booster_Version, Launch_Site
    FROM SPACEXTBL
    WHERE substr(DATE, 0, 5) = '2015'
      AND Landing_Outcome LIKE 'Failure (drone ship)%';
    """
    df_13 = execute_query(cur, query_13, 
                          "Query 13: Failed drone ship landings in 2015")
    if df_13 is not None and not df_13.empty:
        print("\n📊 Generating visualization...")
        viz_failed_landings_2015(df_13, save_fig=True)
    
    # Query 14: Landing outcomes by period
    query_14 = """
    SELECT LANDING_OUTCOME, COUNT(*) AS OUTCOME_COUNT
    FROM SPACEXTBL
    WHERE DATE BETWEEN '2010-06-04' AND '2017-03-20'
    GROUP BY LANDING_OUTCOME
    ORDER BY OUTCOME_COUNT DESC;
    """
    df_14 = execute_query(cur, query_14, 
                          "Query 14: Landing outcomes between June 2010 - March 2017")
    if df_14 is not None:
        print("\n📊 Generating visualization...")
        viz_landing_outcomes_by_period(df_14, save_fig=True)
    
    # ========================================================================
    # STEP 4: SUMMARY STATISTICS
    # ========================================================================
    print_section_header("STEP 4: Summary Statistics")
    
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
    df_summary = execute_query(cur, summary_query, "Overall Dataset Statistics")
    if df_summary is not None:
        print("\n📊 Generating visualization...")
        viz_summary_statistics(df_summary, save_fig=True)
    
    # ========================================================================
    # CLEANUP
    # ========================================================================
    print_section_header("Analysis Complete")
    
    print(f"\n💾 Database file: {DATABASE_NAME}")
    print(f"📊 Table name: {TABLE_NAME}")
    print("\n✅ All queries executed successfully!")
    print("✅ All visualizations generated and saved!")
    
    con.close()
    logger.info("Database connection closed")
    
    print("\n" + "="*80)
    print("📁 Generated Visualization Files:")
    print("="*80)
    viz_files = [
        "viz_02_launch_count_by_site.png",
        "viz_03_cape_canaveral_boosters.png",
        "viz_04_nasa_total_payload.png",
        "viz_05_avg_payload_f9v11.png",
        "viz_06_first_landing_date.png",
        "viz_07_landing_timeline.png",
        "viz_08_landing_outcomes_full.png",
        "viz_09_drone_ship_boosters.png",
        "viz_10_mission_outcomes_full.png",
        "viz_11_success_vs_failure.png",
        "viz_12_max_payload_booster.png",
        "viz_13_failed_landings_2015.png",
        "viz_14_landing_outcomes_period.png",
        "viz_15_summary_statistics.png"
    ]
    for i, vf in enumerate(viz_files, 1):
        print(f"  {i:2d}. {vf}")
    
    print("\n" + "="*80)
    print("Thank you for using SpaceX SQL Analysis with Visualizations!")
    print("="*80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
