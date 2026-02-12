# SpaceX API Data Collection Scripts

## 📋 Overview

These Python scripts collect and process SpaceX Falcon 9 launch data from the SpaceX API for machine learning analysis. The goal is to gather data that will help predict if the Falcon 9 first stage will land successfully.

**Original Source:** Jupyter Notebook (`jupyter-labs-spacex-data-collection-api.ipynb`)  
**Converted:** 2026-02-10

## 📁 Files

### 1. `spacex_api_collection_clean.py` ⭐ **RECOMMENDED**
Production-ready script with clean, modular code.

**Features:**
- ✅ Clear step-by-step execution flow
- ✅ Progress indicators and status messages
- ✅ Comprehensive error handling
- ✅ Formatted output and summary statistics
- ✅ Automatic CSV export
- ✅ Optimized for readability and maintenance

**Use this for:** Running the data collection, integrating into pipelines, production use

### 2. `spacex_api_collection_with_markdown.py`
Direct notebook-to-script conversion with all markdown preserved as comments.

**Features:**
- ✅ Preserves all markdown documentation
- ✅ Maintains original notebook structure
- ✅ Shows educational context and explanations
- ✅ Includes original cell numbering

**Use this for:** Learning, understanding the original notebook, reference

## 🚀 Quick Start

### Installation

```bash
# Required packages
pip install requests pandas numpy
```

### Running the Script

```bash
# Clean version (recommended)
python spacex_api_collection_clean.py

# Markdown version (for reference)
python spacex_api_collection_with_markdown.py
```

## 📊 What the Script Does

### Step 1: API Connection Test
- Tests connection to SpaceX API
- Validates API availability
- Falls back to static JSON if needed

### Step 2: Load Launch Data
- Fetches SpaceX launch data
- Loads from static JSON for consistency
- Normalizes JSON into DataFrame

### Step 3: Data Preprocessing
- Filters to single-core launches (excludes Falcon Heavy)
- Filters to single-payload launches
- Converts dates to proper format
- Filters launches up to November 13, 2020

### Step 4: Extract Detailed Information
Makes additional API calls to get:
- **Booster information:** Version, serial, block, reuse count
- **Payload data:** Mass in kg, target orbit
- **Launch site:** Name, longitude, latitude
- **Core details:** Landing outcome, gridfins, legs, reuse status

### Step 5: Create Final DataFrame
Combines all extracted data into structured format

### Step 6: Data Cleaning
- Removes records with undefined landing outcomes
- Validates data completeness

### Step 7: Save Results
- Exports to CSV (`outputs/spacex_launch_data.csv`)
- Displays summary statistics
- Shows outcome distribution

## 📈 Output

The script produces a CSV file with the following columns:

| Column | Description |
|--------|-------------|
| `FlightNumber` | Sequential flight number |
| `Date` | Launch date |
| `BoosterVersion` | Falcon 9 booster version (e.g., "Falcon 9") |
| `PayloadMass` | Payload mass in kg |
| `Orbit` | Target orbit (LEO, GTO, ISS, etc.) |
| `LaunchSite` | Launch site name |
| `Outcome` | Landing outcome (success/failure + type) |
| `Flights` | Number of flights with this core |
| `GridFins` | Whether gridfins were used (True/False) |
| `Reused` | Whether core was reused (True/False) |
| `Legs` | Whether landing legs were deployed |
| `LandingPad` | Landing pad identifier |
| `Block` | Core block version |
| `ReusedCount` | Number of times core has been reused |
| `Serial` | Core serial number |
| `Longitude` | Launch site longitude |
| `Latitude` | Launch site latitude |

## 📊 Sample Output

```
================================================================================
 SpaceX Falcon 9 Landing Prediction - Data Collection
================================================================================

--------------------------------------------------------------------------------
 Step 1: Testing SpaceX API Connection
--------------------------------------------------------------------------------

🔗 Testing connection to SpaceX API...
✅ API Response Status: 200
📊 Response Size: 1,234,567 bytes

--------------------------------------------------------------------------------
 Step 2: Loading Launch Data
--------------------------------------------------------------------------------

📥 Loading SpaceX launch data from static JSON...
✅ Status Code: 200
📊 Data Size: 234,567 bytes
✅ Loaded 90 launch records

--------------------------------------------------------------------------------
 Step 3: Data Preprocessing
--------------------------------------------------------------------------------

🔧 Preprocessing data...
   Selected 6 key columns
   Removed 10 multi-core launches (Falcon Heavy)
   Removed 2 multi-payload launches
   Extracted single core and payload IDs
   Filtered launches up to 2020-11-13
✅ Final dataset: 78 launches

...

📊 Landing Outcome Distribution:
True ASDS           20
True RTLS           15
False ASDS          10
True Ocean           8
False RTLS           5
...
```

## 🔧 Customization

### Change Date Filter

```python
# In the script, modify:
CUTOFF_DATE = datetime.date(2020, 11, 13)

# To your desired date:
CUTOFF_DATE = datetime.date(2023, 12, 31)
```

### Change Output Location

```python
# Modify the OUTPUT_DIR variable:
OUTPUT_DIR = Path('outputs')

# To:
OUTPUT_DIR = Path('/your/custom/path')
```

### Add Additional Filtering

After line with `data = data[data['date'] <= CUTOFF_DATE]`, add:

```python
# Filter by specific launch site
data = data[data['launchpad'] == 'specific_id']

# Filter by booster version
data = data[data['rocket'] == 'specific_rocket_id']
```

## ⚠️ Important Notes

### API Rate Limits
The script makes multiple API calls (4 per launch record). For ~80 launches:
- Total API calls: ~320
- Estimated time: 2-5 minutes
- SpaceX API is generally permissive, but be respectful

### Data Consistency
The script uses a **static JSON file** by default for consistency across runs and to avoid API changes affecting results. This is the recommended approach for reproducibility.

### Landing Outcomes
Landing outcomes follow this format: `{success_boolean} {landing_type}`

Examples:
- `True ASDS` - Successful autonomous spaceport drone ship landing
- `True RTLS` - Successful return to launch site landing
- `False ASDS` - Failed drone ship landing
- `True Ocean` - Successful controlled ocean landing
- `False Ocean` - Failed ocean landing

## 📚 Data Schema Details

### Booster Versions
- Falcon 9 v1.0
- Falcon 9 v1.1
- Falcon 9 FT (Full Thrust)
- Falcon 9 Block 5

### Orbits
- LEO - Low Earth Orbit
- GTO - Geosynchronous Transfer Orbit
- ISS - International Space Station
- SSO - Sun-Synchronous Orbit
- PO - Polar Orbit
- ES-L1 - Earth-Sun Lagrange Point 1

### Launch Sites
- CCAFS SLC-40 - Cape Canaveral Air Force Station Space Launch Complex 40
- CCAFS LC-40 - Cape Canaveral Air Force Station Launch Complex 40
- KSC LC-39A - Kennedy Space Center Launch Complex 39A
- VAFB SLC-4E - Vandenberg Air Force Base Space Launch Complex 4E

## 🐛 Troubleshooting

### Connection Errors
```
Error connecting to API: Connection refused
```
**Solution:** Check internet connection; script will automatically use static JSON

### Import Errors
```
ModuleNotFoundError: No module named 'requests'
```
**Solution:** `pip install requests pandas numpy`

### Empty DataFrame
```
Final dataset: 0 launches
```
**Solution:** Check date filter; ensure CUTOFF_DATE is in the future relative to launches

### API Timeout
```
Timeout error during API calls
```
**Solution:** Increase timeout in requests:
```python
response = requests.get(url, timeout=30)
```

## 📈 Next Steps

After collecting the data, typical next steps include:

1. **Exploratory Data Analysis (EDA)**
   - Visualize landing success rates
   - Analyze payload vs. success correlation
   - Study launch site performance

2. **Feature Engineering**
   - Create binary classification labels
   - Encode categorical variables
   - Normalize numerical features

3. **Machine Learning**
   - Train classification models
   - Predict landing success
   - Optimize model parameters

## 🤝 Contributing

To improve the script:
1. Add more robust error handling
2. Implement retry logic for failed API calls
3. Add data validation checks
4. Create visualization functions
5. Add logging instead of print statements

## 📄 License

Based on IBM Coursera Data Science Capstone Project materials.

## 🙏 Acknowledgments

- **IBM** - Original Jupyter notebook and course content
- **SpaceX** - Publicly available API
- **Coursera** - Educational platform

---

**Note:** This data represents historical SpaceX launches through November 2020. For current data, modify the `CUTOFF_DATE` or use the live API.
