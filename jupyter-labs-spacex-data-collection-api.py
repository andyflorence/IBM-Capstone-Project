"""
SpaceX Falcon 9 First Stage Landing Prediction - Data Collection via API
==========================================================================

This script collects SpaceX launch data from the SpaceX API and processes it
for machine learning analysis. The goal is to predict if the Falcon 9 first
stage will land successfully.

Background:
-----------
SpaceX advertises Falcon 9 rocket launches at $62 million, while other providers
cost upward of $165 million. Much of the savings comes from reusing the first
stage. By predicting landing success, we can determine launch costs.

Objectives:
-----------
1. Request data from the SpaceX API
2. Clean and format the requested data
3. Extract relevant features for prediction
4. Visualize landing outcome distribution as a pie chart

Data Sources:
-------------
- SpaceX API: https://api.spacexdata.com/v4/launches/past
- Static JSON: For consistent results across runs

Features Extracted:
-------------------
- Booster version and serial
- Payload mass and orbit
- Launch site (name, longitude, latitude)
- Core information (flights, reuse, gridfins, legs)
- Landing outcome and landing pad

Original: Jupyter Notebook (IBM Coursera Capstone)
Converted to: Python Script
Updated:  Added Step 8 - Landing Outcome Pie Chart (matplotlib)
Date: 2026-02-10
"""

#%% IMPORTS AND SETUP

import requests
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import sys

# Display settings
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Configuration
SPACEX_API_URL = 'https://api.spacexdata.com/v4/launches/past'
STATIC_JSON_URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json'
CUTOFF_DATE = datetime.date(2020, 11, 13)

# Output paths
OUTPUT_DIR = Path('outputs')
OUTPUT_DIR.mkdir(exist_ok=True)


#%% UTILITY FUNCTIONS

def section_header(title, char='='):
    """Print formatted section header."""
    print(f"\n{char * 80}")
    print(f" {title}")
    print(f"{char * 80}\n")


#%% DATA EXTRACTION FUNCTIONS

# These functions extract specific information from API responses and 
# populate global lists that will be used to create the final dataframe

def getBoosterVersion(data):
    """Extract booster version from rocket API data."""
    for x in data['rocket']:
        response = requests.get(f"https://api.spacexdata.com/v4/rockets/{x}").json()
        BoosterVersion.append(response['name'])


def getLaunchSite(data):
    """Extract launch site details (name, longitude, latitude)."""
    for x in data['launchpad']:
        response = requests.get(f"https://api.spacexdata.com/v4/launchpads/{x}").json()
        Longitude.append(response['longitude'])
        Latitude.append(response['latitude'])
        LaunchSite.append(response['name'])


def getPayloadData(data):
    """Extract payload mass and orbit information."""
    for load in data['payloads']:
        response = requests.get(f"https://api.spacexdata.com/v4/payloads/{load}").json()
        PayloadMass.append(response['mass_kg'])
        Orbit.append(response['orbit'])


def getCoreData(data):
    """Extract core information including landing outcome and reuse details."""
    for core in data['cores']:
        if core['core'] is not None:
            response = requests.get(f"https://api.spacexdata.com/v4/cores/{core['core']}").json()
            Block.append(response.get('block'))
            ReusedCount.append(response.get('reuse_count'))
            Serial.append(response.get('serial'))
        else:
            Block.append(None)
            ReusedCount.append(None)
            Serial.append(None)

        Outcome.append(str(core.get('landing_success')) + ' ' + str(core.get('landing_type')))
        Flights.append(core.get('flight'))
        GridFins.append(core.get('gridfins'))
        Reused.append(core.get('reused'))
        Legs.append(core.get('legs'))
        LandingPad.append(core.get('landpad'))  # correct API field name


#%% MAIN EXECUTION

def main():
    """Main execution function."""
    
    section_header("SpaceX Falcon 9 Landing Prediction - Data Collection")
    
    # =========================================================================
    # STEP 1: API CONNECTION TEST
    # =========================================================================
    section_header("Step 1: Testing SpaceX API Connection", "-")
    
    print("🔗 Testing connection to SpaceX API...")
    try:
        response = requests.get(SPACEX_API_URL)
        print(f"✅ API Response Status: {response.status_code}")
        print(f"📊 Response Size: {len(response.content):,} bytes")
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")
        print("⚠️  Will use static JSON file instead")
    
    # =========================================================================
    # STEP 2: LOAD DATA FROM STATIC JSON
    # =========================================================================
    section_header("Step 2: Loading Launch Data", "-")
    
    print("📥 Loading SpaceX launch data from static JSON...")
    try:
        response = requests.get(STATIC_JSON_URL)
        print(f"✅ Status Code: {response.status_code}")
        print(f"📊 Data Size: {len(response.content):,} bytes")
        
        # Convert to dataframe
        data = response.json()
        data = pd.json_normalize(data)
        print(f"✅ Loaded {len(data)} launch records")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        sys.exit(1)
    
    # =========================================================================
    # STEP 3: DATA PREPROCESSING
    # =========================================================================
    section_header("Step 3: Data Preprocessing", "-")
    
    print("🔧 Preprocessing data...")
    
    # Keep only relevant columns
    data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]
    print(f"   Selected {len(data.columns)} key columns")
    
    # Remove rows with multiple cores (Falcon Heavy)
    initial_count = len(data)
    data = data[data['cores'].map(len) == 1]
    print(f"   Removed {initial_count - len(data)} multi-core launches (Falcon Heavy)")
    
    # Remove rows with multiple payloads
    initial_count = len(data)
    data = data[data['payloads'].map(len) == 1]
    print(f"   Removed {initial_count - len(data)} multi-payload launches")
    
    # Extract single values from lists
    data['cores'] = data['cores'].map(lambda x: x[0])
    data['payloads'] = data['payloads'].map(lambda x: x[0])
    print("   Extracted single core and payload IDs")
    
    # Convert date and filter
    data['date'] = pd.to_datetime(data['date_utc']).dt.date
    data = data[data['date'] <= CUTOFF_DATE]
    print(f"   Filtered launches up to {CUTOFF_DATE}")
    print(f"✅ Final dataset: {len(data)} launches")
    
    # =========================================================================
    # STEP 4: EXTRACT DETAILED INFORMATION
    # =========================================================================
    section_header("Step 4: Extracting Detailed Information", "-")
    
    # Initialize global lists
    global BoosterVersion, PayloadMass, Orbit, LaunchSite
    global Outcome, Flights, GridFins, Reused, Legs, LandingPad
    global Block, ReusedCount, Serial, Longitude, Latitude
    
    BoosterVersion = []
    PayloadMass = []
    Orbit = []
    LaunchSite = []
    Outcome = []
    Flights = []
    GridFins = []
    Reused = []
    Legs = []
    LandingPad = []
    Block = []
    ReusedCount = []
    Serial = []
    Longitude = []
    Latitude = []
    
    print("⏳ Fetching detailed information from API...")
    print("   This may take a few minutes...")
    
    try:
        # Extract booster information
        print("\n   📡 Fetching booster versions...")
        getBoosterVersion(data)
        print(f"   ✅ Extracted {len(BoosterVersion)} booster versions")
        
        # Extract launch site information
        print("   📡 Fetching launch sites...")
        getLaunchSite(data)
        print(f"   ✅ Extracted {len(LaunchSite)} launch sites")
        
        # Extract payload information
        print("   📡 Fetching payload data...")
        getPayloadData(data)
        print(f"   ✅ Extracted {len(PayloadMass)} payload records")
        
        # Extract core information
        print("   📡 Fetching core data...")
        getCoreData(data)
        print(f"   ✅ Extracted {len(Outcome)} core records")
        
    except Exception as e:
        print(f"   ❌ Error during API extraction: {e}")
        sys.exit(1)
    
    # =========================================================================
    # STEP 5: CREATE FINAL DATAFRAME
    # =========================================================================
    section_header("Step 5: Creating Final Dataset", "-")
    
    print("🔨 Building final dataframe...")
    
    # Create dictionary with all extracted data
    launch_dict = {
        'FlightNumber': list(data['flight_number']),
        'Date': list(data['date']),
        'BoosterVersion': BoosterVersion,
        'PayloadMass': PayloadMass,
        'Orbit': Orbit,
        'LaunchSite': LaunchSite,
        'Outcome': Outcome,
        'Flights': Flights,
        'GridFins': GridFins,
        'Reused': Reused,
        'Legs': Legs,
        'LandingPad': LandingPad,
        'Block': Block,
        'ReusedCount': ReusedCount,
        'Serial': Serial,
        'Longitude': Longitude,
        'Latitude': Latitude
    }
    
    # Create dataframe
    df = pd.DataFrame(launch_dict)
    
    print(f"✅ Created dataframe with {len(df)} rows and {len(df.columns)} columns")
    
    # =========================================================================
    # STEP 6: DATA CLEANING
    # =========================================================================
    section_header("Step 6: Data Cleaning", "-")
    
    # Filter out landing outcomes with None values
    print("🧹 Cleaning landing outcomes...")
    initial_count = len(df)
    df = df[df['Outcome'].str.contains('None') == False]
    print(f"   Removed {initial_count - len(df)} records with undefined outcomes")
    print(f"✅ Final dataset: {len(df)} launches")
    
    # =========================================================================
    # STEP 7: SAVE AND DISPLAY RESULTS
    # =========================================================================
    section_header("Step 7: Results", "-")
    
    # Display summary statistics
    print("📊 Dataset Summary:")
    print(f"   Total Launches: {len(df)}")
    print(f"   Date Range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"   Launch Sites: {df['LaunchSite'].nunique()}")
    print(f"   Booster Types: {df['BoosterVersion'].nunique()}")
    print(f"   Unique Outcomes: {df['Outcome'].nunique()}")
    
    print("\n📋 First 5 records:")
    print(df.head().to_string())
    
    print("\n📋 Data Types:")
    print(df.dtypes)
    
    print("\n📋 Missing Values:")
    print(df.isnull().sum())
    
    # Save to CSV
    output_file = OUTPUT_DIR / 'jupyter-labs-spacex-data-collection-api.spacex_launch_data.csv'
    df.to_csv(output_file, index=False)
    print(f"\n💾 Saved dataset to: {output_file}")
    
    # Display outcome distribution
    print("\n📊 Landing Outcome Distribution:")
    print(df['Outcome'].value_counts().to_string())
    
    # =========================================================================
    # STEP 8: LANDING OUTCOME PIE CHART
    # =========================================================================
    section_header("Step 8: Landing Outcome Pie Chart", "-")

    print("📊 Generating landing outcome pie chart...")

    # Compute outcome counts
    outcome_counts = df['Outcome'].value_counts()

    # Color palette: greens for successful landings, reds/oranges for failures
    def outcome_color(label):
        label_lower = label.lower()
        if 'true' in label_lower:
            return '#2ecc71'   # green  – successful landing
        elif 'false' in label_lower:
            return '#e74c3c'   # red    – failed landing
        else:
            return '#95a5a6'   # grey   – unknown / other

    colors = [outcome_color(lbl) for lbl in outcome_counts.index]

    # Explode the largest slice slightly for emphasis
    explode = [0.05 if i == 0 else 0 for i in range(len(outcome_counts))]

    fig, ax = plt.subplots(figsize=(10, 7))

    wedges, texts, autotexts = ax.pie(
        outcome_counts,
        labels=None,            # labels handled via legend for readability
        autopct=lambda pct: f'{pct:.1f}%\n({int(round(pct / 100 * outcome_counts.sum()))})',
        colors=colors,
        explode=explode,
        startangle=140,
        pctdistance=0.75,
        wedgeprops=dict(edgecolor='white', linewidth=1.5)
    )

    # Style percentage text
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    # Legend with full outcome labels
    legend_patches = [
        mpatches.Patch(color=colors[i], label=f'{outcome_counts.index[i]}  ({outcome_counts.iloc[i]})')
        for i in range(len(outcome_counts))
    ]
    ax.legend(
        handles=legend_patches,
        title='Outcome (count)',
        title_fontsize=10,
        fontsize=9,
        loc='lower left',
        bbox_to_anchor=(-0.25, -0.05)
    )

    ax.set_title(
        'SpaceX Falcon 9 — First Stage Landing Outcome Distribution',
        fontsize=14,
        fontweight='bold',
        pad=20
    )

    # Summary annotation
    total    = len(df)
    n_success = outcome_counts[outcome_counts.index.str.contains('True')].sum()
    n_fail    = total - n_success
    fig.text(
        0.5, 0.01,
        f'Total launches: {total}  |  Successful landings: {n_success}  |  Failed/Other: {n_fail}',
        ha='center', fontsize=9, color='#555555'
    )

    plt.tight_layout()

    # Save chart
    chart_file = OUTPUT_DIR / 'spacex_landing_outcome_pie_chart.png'
    plt.savefig(chart_file, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ Pie chart saved to: {chart_file}")

    section_header("Data Collection Complete! ✅")

    return df


if __name__ == "__main__":
    try:
        df_spacex = main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Data collection interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
