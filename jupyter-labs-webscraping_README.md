# SpaceX Falcon 9 Launch Data Web Scraper

A Python web scraping tool that extracts Falcon 9 and Falcon Heavy launch records from Wikipedia. This tool parses historical launch data including flight numbers, dates, booster versions, launch sites, payloads, and landing outcomes.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Code Review & Optimizations](#code-review--optimizations)
- [Output Data](#output-data)
- [Project Structure](#project-structure)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Overview

This project scrapes launch data from a static Wikipedia snapshot (dated June 9, 2021) of Falcon 9 and Falcon Heavy launches. The data is extracted, cleaned, and exported to a CSV file for further analysis and machine learning applications, particularly for predicting first stage landing success.

**Data Source:** [List of Falcon 9 and Falcon Heavy launches - Wikipedia](https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922)

## ✨ Features

- **Automated web scraping** from Wikipedia using BeautifulSoup4
- **Comprehensive data extraction** including:
  - Flight numbers
  - Launch dates and times
  - Booster versions
  - Launch sites
  - Payload information and mass
  - Orbit types
  - Customer details
  - Launch outcomes
  - Booster landing status
- **Robust error handling** with logging
- **Data validation** and cleaning
- **CSV export** for easy data analysis
- **Type hints** for better code maintainability
- **Modular design** with well-documented functions

## 📦 Requirements

### Python Version
- Python 3.7 or higher

### Dependencies
```
beautifulsoup4>=4.9.0
requests>=2.25.0
pandas>=1.2.0
```

## 🔧 Installation

### 1. Clone or Download the Repository

```bash
git clone <repository-url>
cd spacex-launch-scraper
```

### 2. Install Dependencies

#### Using pip:
```bash
pip install beautifulsoup4 requests pandas
```

#### Using requirements.txt:
```bash
pip install -r requirements.txt
```

#### Using conda:
```bash
conda install beautifulsoup4 requests pandas
```

## 💻 Usage

### Basic Usage

Run the script directly:

```bash
python spacex_launch_scraper.py
```

### Importing as a Module

```python
from spacex_launch_scraper import main

# Run the scraper
df = main()

# Access the data
print(df.head())
print(f"Total launches: {len(df)}")
```

### Custom Output File

Modify the `output_file` variable in the `main()` function:

```python
output_file = "my_custom_name.csv"
save_to_csv(df, output_file)
```

## 🔍 Code Review & Optimizations

### Issues Found in Original Code

1. **Dependency Installation**: The original code attempted to install packages programmatically, which can fail in managed environments
2. **Error Handling**: Limited error handling for network issues or parsing errors
3. **Magic Numbers**: Table index (2) was hardcoded without explanation
4. **No Logging**: Difficult to debug issues
5. **Incomplete Documentation**: Missing docstrings and type hints
6. **Data Validation**: No validation for incomplete rows

### Optimizations Implemented

#### 1. **Removed Automatic Package Installation**
```python
# ❌ Original (problematic)
subprocess.check_call([sys.executable, "-m", "pip", "install", ...])

# ✅ Optimized (rely on proper environment setup)
# Packages should be installed via requirements.txt
```

#### 2. **Added Comprehensive Logging**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

#### 3. **Enhanced Error Handling**
```python
try:
    extracted_row += 1
    # ... extraction logic ...
except Exception as e:
    logger.error(f"Error processing flight {flight_number}: {e}")
    # Clean up partial data
    for key in launch_dict:
        if len(launch_dict[key]) == extracted_row:
            launch_dict[key].pop()
    extracted_row -= 1
```

#### 4. **Added Type Hints**
```python
def extract_column_names(table) -> List[str]:
    """Extract column names from table header."""
    ...

def create_dataframe(launch_dict: Dict[str, List]) -> pd.DataFrame:
    """Create pandas DataFrame from launch dictionary."""
    ...
```

#### 5. **Modular Function Design**
The code is now organized into logical functions:
- `fetch_wikipedia_page()`: Handles HTTP requests
- `extract_column_names()`: Parses table headers
- `parse_launch_tables()`: Main extraction logic
- `create_dataframe()`: Data structuring
- `save_to_csv()`: Output handling

#### 6. **Data Validation**
```python
if len(row) < 9:  # Ensure row has enough columns
    logger.warning(f"Skipping incomplete row for flight {flight_number}")
    continue
```

#### 7. **Better Default Values**
```python
# Handle missing data gracefully
launch_site = row[2].a.string if row[2].a else row[2].get_text(strip=True)
bv = booster_version(row[1]) or "Unknown"
```

#### 8. **Improved Summary Output**
```python
print("\n" + "="*80)
print("SPACEX LAUNCH DATA EXTRACTION SUMMARY")
print("="*80)
print(f"\nTotal records extracted: {len(df)}")
print(df.dtypes)
print(df.isnull().sum())
```

## 📊 Output Data

### CSV Columns

| Column | Description | Example |
|--------|-------------|---------|
| Flight No. | Sequential flight number | "1", "2", "3" |
| Date | Launch date | "4 June 2010" |
| Time | Launch time (UTC) | "18:45" |
| Version Booster | Booster version identifier | "F9 v1.0B0003.1" |
| Launch site | Launch facility | "CCAFS SLC-40" |
| Payload | Payload name | "Dragon Spacecraft Qualification Unit" |
| Payload mass | Mass with unit | "0 kg" |
| Orbit | Target orbit | "LEO" |
| Customer | Customer/organization | "SpaceX" |
| Launch outcome | Success/failure status | "Success" |
| Booster landing | Landing outcome | "Failure" |

### Sample Output

```
Flight No.  Date           Time   Version Booster      Launch site  ...
1           4 June 2010    18:45  F9 v1.0B0003.1      CCAFS SLC-40  ...
2           8 December 2010 15:43 F9 v1.0B0004.1      CCAFS SLC-40  ...
...
```

## 📁 Project Structure

```
spacex-launch-scraper/
│
├── spacex_launch_scraper.py    # Optimized main script
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── spacex_launches.csv          # Output file (generated)
│
└── original/
    └── jupyter-labs-webscraping_spacex.py  # Original script
```

## ⚠️ Error Handling

### Network Errors
The script handles network timeouts and connection errors:
```python
response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()
```

### Parsing Errors
Individual row failures don't stop the entire scrape:
```python
try:
    # Extract data
except Exception as e:
    logger.error(f"Error processing flight {flight_number}: {e}")
    # Continue with next row
```

### Missing Data
The script gracefully handles missing values:
- Returns "Unknown" for missing booster versions
- Returns "0" for missing payload mass
- Logs warnings for incomplete rows

## 🐛 Known Limitations

1. **Static Snapshot**: Data is from June 9, 2021 - does not include recent launches
2. **Wikipedia Dependency**: Changes to Wikipedia's HTML structure may break parsing
3. **Rate Limiting**: No rate limiting implemented (not needed for static snapshot)
4. **Language**: Only supports English Wikipedia

## 🔄 Future Improvements

- [ ] Add support for live Wikipedia pages
- [ ] Implement caching mechanism
- [ ] Add data visualization
- [ ] Create unit tests
- [ ] Add support for other launch providers
- [ ] Implement incremental updates
- [ ] Add database storage option
- [ ] Create REST API wrapper

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is provided as-is for educational purposes. Please respect Wikipedia's [Terms of Use](https://foundation.wikimedia.org/wiki/Terms_of_Use) when using this scraper.

## 🙏 Acknowledgments

- Data source: [Wikipedia - List of Falcon 9 and Falcon Heavy launches](https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches)
- SpaceX for making launch data publicly available
- Beautiful Soup documentation and community

## 📧 Contact

For questions or suggestions, please open an issue in the repository.

---

**Last Updated:** February 2026
**Python Version:** 3.7+
**Status:** Active Development
