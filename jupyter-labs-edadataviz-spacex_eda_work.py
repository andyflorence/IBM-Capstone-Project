"""
SpaceX Falcon 9 Launch Data - Exploratory Data Analysis and Visualization

This script performs comprehensive exploratory data analysis (EDA) on SpaceX Falcon 9 
launch data to understand factors affecting first-stage landing success.

Objectives:
- Analyze relationships between flight characteristics and landing outcomes
- Visualize patterns in launch sites, payload mass, orbits, and flight numbers
- Generate insights for predictive modeling

Author: Converted and optimized from Jupyter Notebook
Date: February 2026
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from typing import Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10


# ============================================================================
# Data Loading Functions
# ============================================================================

def load_data(filepath: str) -> pd.DataFrame:
    """
    Load SpaceX launch data from CSV file.
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        pandas DataFrame with launch data
    """
    try:
        logger.info(f"Loading data from {filepath}")
        df = pd.read_csv(filepath)
        logger.info(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise


def inspect_data(df: pd.DataFrame) -> None:
    """
    Display basic information about the dataset.
    
    Args:
        df: Input DataFrame
    """
    print("\n" + "="*80)
    print("DATASET OVERVIEW")
    print("="*80)
    
    print(f"\nShape: {df.shape[0]} rows × {df.shape[1]} columns")
    
    print("\nColumn Names:")
    print(df.columns.tolist())
    
    print("\nData Types:")
    print(df.dtypes)
    
    print("\nFirst 5 Rows:")
    print(df.head())
    
    print("\nDataset Info:")
    df.info()
    
    print("\nMissing Values:")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
    else:
        print("No missing values found")
    
    print("\nBasic Statistics:")
    print(df.describe())
    
    if 'Class' in df.columns:
        print("\nClass Distribution (Landing Outcome):")
        print(df['Class'].value_counts())
        print(f"\nSuccess Rate: {df['Class'].mean():.2%}")
    
    print("\n" + "="*80 + "\n")


# ============================================================================
# Exploratory Data Analysis Functions
# ============================================================================

def plot_flight_vs_payload(df: pd.DataFrame, save_fig: bool = False) -> None:
    """
    Visualize relationship between Flight Number, Payload Mass, and Landing Class.
    
    Shows how launch success improves with flight number and payload mass.
    
    Args:
        df: Input DataFrame
        save_fig: Whether to save figure to file
    """
    logger.info("Creating Flight Number vs Payload Mass visualization")
    
    plt.figure(figsize=(14, 6))
    sns.scatterplot(
        data=df,
        x="FlightNumber",
        y="PayloadMass",
        hue="Class",
        palette={0: 'red', 1: 'green'},
        s=100,
        alpha=0.7
    )
    
    plt.xlabel("Flight Number", fontsize=14)
    plt.ylabel("Payload Mass (kg)", fontsize=14)
    plt.title("Flight Number vs Payload Mass by Landing Outcome", fontsize=16)
    plt.legend(title="Landing Success", labels=['Failed (0)', 'Success (1)'])
    plt.grid(True, alpha=0.3)
    
    if save_fig:
        plt.savefig('flight_vs_payload.png', dpi=300, bbox_inches='tight')
        logger.info("Figure saved: flight_vs_payload.png")
    
    plt.show()


def plot_flight_vs_launchsite(df: pd.DataFrame, save_fig: bool = False) -> None:
    """
    Visualize relationship between Flight Number and Launch Site.
    
    Shows launch patterns across different launch sites over time.
    
    Args:
        df: Input DataFrame
        save_fig: Whether to save figure to file
    """
    logger.info("Creating Flight Number vs Launch Site visualization")
    
    plt.figure(figsize=(14, 6))
    sns.scatterplot(
        data=df,
        x="FlightNumber",
        y="LaunchSite",
        hue="Class",
        palette={0: 'red', 1: 'green'},
        s=100,
        alpha=0.7
    )
    
    plt.xlabel("Flight Number", fontsize=14)
    plt.ylabel("Launch Site", fontsize=14)
    plt.title("Flight Number vs Launch Site by Landing Outcome", fontsize=16)
    plt.legend(title="Landing Success", labels=['Failed (0)', 'Success (1)'])
    plt.grid(True, alpha=0.3, axis='x')
    
    if save_fig:
        plt.savefig('flight_vs_launchsite.png', dpi=300, bbox_inches='tight')
        logger.info("Figure saved: flight_vs_launchsite.png")
    
    plt.show()


def plot_payload_vs_launchsite(df: pd.DataFrame, save_fig: bool = False) -> None:
    """
    Visualize relationship between Payload Mass and Launch Site.
    
    Shows which launch sites handle different payload masses.
    
    Args:
        df: Input DataFrame
        save_fig: Whether to save figure to file
    """
    logger.info("Creating Payload Mass vs Launch Site visualization")
    
    plt.figure(figsize=(14, 6))
    sns.scatterplot(
        data=df,
        x="PayloadMass",
        y="LaunchSite",
        hue="Class",
        palette={0: 'red', 1: 'green'},
        s=100,
        alpha=0.7
    )
    
    plt.xlabel("Payload Mass (kg)", fontsize=14)
    plt.ylabel("Launch Site", fontsize=14)
    plt.title("Payload Mass vs Launch Site by Landing Outcome", fontsize=16)
    plt.legend(title="Landing Success", labels=['Failed (0)', 'Success (1)'])
    plt.grid(True, alpha=0.3, axis='x')
    
    if save_fig:
        plt.savefig('payload_vs_launchsite.png', dpi=300, bbox_inches='tight')
        logger.info("Figure saved: payload_vs_launchsite.png")
    
    plt.show()


def plot_success_rate_by_orbit(df: pd.DataFrame, save_fig: bool = False) -> None:
    """
    Visualize success rate for each orbit type.
    
    Shows which orbits have the highest landing success rates.
    
    Args:
        df: Input DataFrame
        save_fig: Whether to save figure to file
    """
    logger.info("Creating Success Rate by Orbit visualization")
    
    # Calculate success rate by orbit
    orbit_success = df.groupby("Orbit")["Class"].agg(['mean', 'count']).reset_index()
    orbit_success.columns = ['Orbit', 'SuccessRate', 'Count']
    orbit_success = orbit_success.sort_values('SuccessRate', ascending=False)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Success rate bar chart
    bars = ax1.bar(
        range(len(orbit_success)),
        orbit_success['SuccessRate'],
        color=plt.cm.RdYlGn(orbit_success['SuccessRate'])
    )
    ax1.set_xticks(range(len(orbit_success)))
    ax1.set_xticklabels(orbit_success['Orbit'], rotation=45, ha='right')
    ax1.set_xlabel("Orbit Type", fontsize=14)
    ax1.set_ylabel("Success Rate", fontsize=14)
    ax1.set_title("Landing Success Rate by Orbit Type", fontsize=16)
    ax1.set_ylim(0, 1)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for i, (bar, rate) in enumerate(zip(bars, orbit_success['SuccessRate'])):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f'{rate:.1%}', ha='center', va='bottom', fontsize=9)
    
    # Launch count by orbit
    ax2.bar(range(len(orbit_success)), orbit_success['Count'], color='steelblue')
    ax2.set_xticks(range(len(orbit_success)))
    ax2.set_xticklabels(orbit_success['Orbit'], rotation=45, ha='right')
    ax2.set_xlabel("Orbit Type", fontsize=14)
    ax2.set_ylabel("Number of Launches", fontsize=14)
    ax2.set_title("Launch Count by Orbit Type", fontsize=16)
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_fig:
        plt.savefig('success_rate_by_orbit.png', dpi=300, bbox_inches='tight')
        logger.info("Figure saved: success_rate_by_orbit.png")
    
    plt.show()
    
    # Print summary
    print("\nOrbit Success Rate Summary:")
    print(orbit_success.to_string(index=False))


def plot_flight_vs_orbit(df: pd.DataFrame, save_fig: bool = False) -> None:
    """
    Visualize relationship between Flight Number and Orbit type.
    
    Shows how orbit selection evolved over time.
    
    Args:
        df: Input DataFrame
        save_fig: Whether to save figure to file
    """
    logger.info("Creating Flight Number vs Orbit visualization")
    
    plt.figure(figsize=(14, 8))
    sns.scatterplot(
        data=df,
        x="FlightNumber",
        y="Orbit",
        hue="Class",
        palette={0: 'red', 1: 'green'},
        s=100,
        alpha=0.7
    )
    
    plt.xlabel("Flight Number", fontsize=14)
    plt.ylabel("Orbit Type", fontsize=14)
    plt.title("Flight Number vs Orbit Type by Landing Outcome", fontsize=16)
    plt.legend(title="Landing Success", labels=['Failed (0)', 'Success (1)'])
    plt.grid(True, alpha=0.3, axis='x')
    
    if save_fig:
        plt.savefig('flight_vs_orbit.png', dpi=300, bbox_inches='tight')
        logger.info("Figure saved: flight_vs_orbit.png")
    
    plt.show()


def plot_payload_vs_orbit(df: pd.DataFrame, save_fig: bool = False) -> None:
    """
    Visualize relationship between Payload Mass and Orbit type.
    
    Shows payload requirements for different orbit types.
    
    Args:
        df: Input DataFrame
        save_fig: Whether to save figure to file
    """
    logger.info("Creating Payload Mass vs Orbit visualization")
    
    plt.figure(figsize=(14, 8))
    sns.scatterplot(
        data=df,
        x="PayloadMass",
        y="Orbit",
        hue="Class",
        palette={0: 'red', 1: 'green'},
        s=100,
        alpha=0.7
    )
    
    plt.xlabel("Payload Mass (kg)", fontsize=14)
    plt.ylabel("Orbit Type", fontsize=14)
    plt.title("Payload Mass vs Orbit Type by Landing Outcome", fontsize=16)
    plt.legend(title="Landing Success", labels=['Failed (0)', 'Success (1)'])
    plt.grid(True, alpha=0.3, axis='x')
    
    if save_fig:
        plt.savefig('payload_vs_orbit.png', dpi=300, bbox_inches='tight')
        logger.info("Figure saved: payload_vs_orbit.png")
    
    plt.show()


def plot_yearly_trends(df: pd.DataFrame, save_fig: bool = False) -> None:
    """
    Visualize launch success trends over years.
    
    Requires a 'Year' column in the DataFrame.
    
    Args:
        df: Input DataFrame
        save_fig: Whether to save figure to file
    """
    if 'Year' not in df.columns:
        logger.warning("Year column not found. Skipping yearly trends plot.")
        return
    
    logger.info("Creating yearly trends visualization")
    
    yearly_stats = df.groupby('Year').agg({
        'Class': ['sum', 'count', 'mean']
    }).reset_index()
    yearly_stats.columns = ['Year', 'Successes', 'Total', 'SuccessRate']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Launch count over time
    ax1.plot(yearly_stats['Year'], yearly_stats['Total'], marker='o', 
             linewidth=2, markersize=8, color='steelblue')
    ax1.set_xlabel("Year", fontsize=14)
    ax1.set_ylabel("Number of Launches", fontsize=14)
    ax1.set_title("Total Launches per Year", fontsize=16)
    ax1.grid(True, alpha=0.3)
    
    # Success rate over time
    ax2.plot(yearly_stats['Year'], yearly_stats['SuccessRate'], marker='o',
             linewidth=2, markersize=8, color='green')
    ax2.set_xlabel("Year", fontsize=14)
    ax2.set_ylabel("Success Rate", fontsize=14)
    ax2.set_title("Landing Success Rate per Year", fontsize=16)
    ax2.set_ylim(0, 1)
    ax2.grid(True, alpha=0.3)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
    
    plt.tight_layout()
    
    if save_fig:
        plt.savefig('yearly_trends.png', dpi=300, bbox_inches='tight')
        logger.info("Figure saved: yearly_trends.png")
    
    plt.show()


def plot_launchsite_comparison(df: pd.DataFrame, save_fig: bool = False) -> None:
    """
    Compare success rates and launch counts across launch sites.
    
    Args:
        df: Input DataFrame
        save_fig: Whether to save figure to file
    """
    logger.info("Creating launch site comparison visualization")
    
    site_stats = df.groupby('LaunchSite').agg({
        'Class': ['sum', 'count', 'mean']
    }).reset_index()
    site_stats.columns = ['LaunchSite', 'Successes', 'Total', 'SuccessRate']
    site_stats = site_stats.sort_values('SuccessRate', ascending=False)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Success rate by site
    bars1 = ax1.barh(site_stats['LaunchSite'], site_stats['SuccessRate'],
                      color=plt.cm.RdYlGn(site_stats['SuccessRate']))
    ax1.set_xlabel("Success Rate", fontsize=14)
    ax1.set_ylabel("Launch Site", fontsize=14)
    ax1.set_title("Landing Success Rate by Launch Site", fontsize=16)
    ax1.set_xlim(0, 1)
    ax1.grid(True, alpha=0.3, axis='x')
    
    for i, (bar, rate) in enumerate(zip(bars1, site_stats['SuccessRate'])):
        ax1.text(rate + 0.02, bar.get_y() + bar.get_height()/2,
                f'{rate:.1%}', va='center', fontsize=10)
    
    # Launch count by site
    ax2.barh(site_stats['LaunchSite'], site_stats['Total'], color='steelblue')
    ax2.set_xlabel("Number of Launches", fontsize=14)
    ax2.set_ylabel("Launch Site", fontsize=14)
    ax2.set_title("Total Launches by Launch Site", fontsize=16)
    ax2.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    
    if save_fig:
        plt.savefig('launchsite_comparison.png', dpi=300, bbox_inches='tight')
        logger.info("Figure saved: launchsite_comparison.png")
    
    plt.show()
    
    print("\nLaunch Site Summary:")
    print(site_stats.to_string(index=False))


def generate_correlation_heatmap(df: pd.DataFrame, save_fig: bool = False) -> None:
    """
    Generate correlation heatmap for numeric features.
    
    Args:
        df: Input DataFrame
        save_fig: Whether to save figure to file
    """
    logger.info("Creating correlation heatmap")
    
    # Select numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) < 2:
        logger.warning("Not enough numeric columns for correlation analysis")
        return
    
    plt.figure(figsize=(10, 8))
    correlation_matrix = df[numeric_cols].corr()
    
    sns.heatmap(
        correlation_matrix,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        center=0,
        square=True,
        linewidths=1,
        cbar_kws={"shrink": 0.8}
    )
    
    plt.title("Feature Correlation Heatmap", fontsize=16)
    plt.tight_layout()
    
    if save_fig:
        plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
        logger.info("Figure saved: correlation_heatmap.png")
    
    plt.show()


# ============================================================================
# Main Analysis Pipeline
# ============================================================================

def run_complete_eda(filepath: str, save_figures: bool = False) -> pd.DataFrame:
    """
    Run complete exploratory data analysis pipeline.
    
    Args:
        filepath: Path to CSV file
        save_figures: Whether to save all figures
        
    Returns:
        DataFrame with loaded data
    """
    logger.info("Starting comprehensive EDA pipeline")
    
    # Load and inspect data
    df = load_data(filepath)
    inspect_data(df)
    
    # Generate all visualizations
    print("\n" + "="*80)
    print("GENERATING VISUALIZATIONS")
    print("="*80 + "\n")
    
    plot_flight_vs_payload(df, save_figures)
    plot_flight_vs_launchsite(df, save_figures)
    plot_payload_vs_launchsite(df, save_figures)
    plot_success_rate_by_orbit(df, save_figures)
    plot_flight_vs_orbit(df, save_figures)
    plot_payload_vs_orbit(df, save_figures)
    plot_yearly_trends(df, save_figures)
    plot_launchsite_comparison(df, save_figures)
    generate_correlation_heatmap(df, save_figures)
    
    logger.info("EDA pipeline completed successfully")
    
    return df


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Main execution function."""
    
    # Configuration
    DATA_FILE = "dataset_part_2.csv"  # Update with your file path
    SAVE_FIGURES = True  # Set to True to save all plots
    
    try:
        # Run complete EDA
        df = run_complete_eda(DATA_FILE, save_figures=SAVE_FIGURES)
        
        print("\n" + "="*80)
        print("KEY FINDINGS SUMMARY")
        print("="*80)
        print(f"\nTotal Launches Analyzed: {len(df)}")
        print(f"Overall Success Rate: {df['Class'].mean():.2%}")
        print(f"\nNumber of Launch Sites: {df['LaunchSite'].nunique()}")
        print(f"Number of Orbit Types: {df['Orbit'].nunique()}")
        print(f"Payload Mass Range: {df['PayloadMass'].min():.0f} - {df['PayloadMass'].max():.0f} kg")
        print(f"Flight Number Range: {df['FlightNumber'].min()} - {df['FlightNumber'].max()}")
        
        if SAVE_FIGURES:
            print(f"\n✓ All visualizations saved to current directory")
        
        print("\n" + "="*80)
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise


if __name__ == "__main__":
    main()
