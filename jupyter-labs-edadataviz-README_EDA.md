# SpaceX Falcon 9 Launch Data - Exploratory Data Analysis

A comprehensive Python script for analyzing SpaceX Falcon 9 launch data to understand factors affecting first-stage landing success. This project performs in-depth exploratory data analysis (EDA) with interactive visualizations to reveal patterns and insights.

## 📋 Table of Contents

- [Overview](#overview)
- [Objectives](#objectives)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Data Description](#data-description)
- [Analysis Components](#analysis-components)
- [Visualizations](#visualizations)
- [Key Findings](#key-findings)
- [Code Structure](#code-structure)
- [Optimization Details](#optimization-details)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🚀 Overview

This project analyzes SpaceX Falcon 9 launch data to identify patterns and relationships that influence first-stage landing success. SpaceX's ability to reuse the first stage is crucial to reducing launch costs from $165M+ to $62M per launch.

**Source:** Converted and optimized from Jupyter Notebook  
**Analysis Type:** Exploratory Data Analysis (EDA) with Statistical Visualizations  
**Primary Goal:** Understand factors predicting successful booster landings

## 🎯 Objectives

The primary objectives of this EDA are to:

- **Understand the structure, patterns, and relationships** within SpaceX launch data through statistical summaries and visualizations
- **Identify data quality issues, discover insights, and generate hypotheses** to inform predictive modeling decisions
- **Analyze relationships** between flight characteristics (payload, orbit, site) and landing outcomes
- **Prepare findings** for subsequent machine learning classification models

## ✨ Features

### Analysis Capabilities
- **Comprehensive data inspection** with automated quality checks
- **Multi-dimensional visualizations** showing relationships between variables
- **Success rate analysis** by orbit type, launch site, and time period
- **Trend analysis** showing evolution of launch success over time
- **Correlation analysis** identifying feature relationships
- **Automated reporting** with key statistics and findings

### Technical Features
- **Modular design** with reusable functions
- **Type hints** for better code clarity
- **Comprehensive logging** for debugging and monitoring
- **Automatic figure saving** option
- **Error handling** with graceful failures
- **Professional visualizations** with publication-quality graphics

## 📦 Requirements

### Python Version
- Python 3.7 or higher

### Dependencies
```
pandas>=1.2.0
numpy>=1.19.0
matplotlib>=3.3.0
seaborn>=0.11.0
```

## 🔧 Installation

### 1. Clone or Download

```bash
git clone <repository-url>
cd spacex-eda-analysis
```

### 2. Install Dependencies

#### Using pip:
```bash
pip install pandas numpy matplotlib seaborn
```

#### Using requirements.txt:
```bash
pip install -r requirements.txt
```

#### Using conda:
```bash
conda install pandas numpy matplotlib seaborn
```

### 3. Prepare Data

Ensure your data file `dataset_part_2.csv` is in the same directory as the script, or update the `DATA_FILE` path in the script.

## 💻 Usage

### Basic Usage

Run the complete analysis pipeline:

```bash
python spacex_eda_visualization.py
```

This will:
1. Load the dataset
2. Display data overview and statistics
3. Generate all visualizations
4. Save figures (if enabled)
5. Print key findings summary

### Customization

Edit the configuration in the `main()` function:

```python
def main():
    # Configuration
    DATA_FILE = "dataset_part_2.csv"  # Update with your file path
    SAVE_FIGURES = True  # Set to False to skip saving
```

### Using Individual Functions

Import and use specific analysis functions:

```python
from spacex_eda_visualization import (
    load_data,
    inspect_data,
    plot_flight_vs_payload,
    plot_success_rate_by_orbit
)

# Load data
df = load_data("dataset_part_2.csv")

# Inspect data
inspect_data(df)

# Generate specific plots
plot_flight_vs_payload(df, save_fig=True)
plot_success_rate_by_orbit(df, save_fig=True)
```

### Jupyter Notebook Integration

Use in Jupyter notebooks for interactive analysis:

```python
%matplotlib inline
import spacex_eda_visualization as eda

df = eda.load_data("dataset_part_2.csv")
eda.plot_success_rate_by_orbit(df)
```

## 📊 Data Description

### Expected Data Format

CSV file with the following columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| FlightNumber | Integer | Sequential flight number | 1, 2, 3... |
| Date | String/Date | Launch date | "2010-06-04" |
| Time | String/Time | Launch time (UTC) | "18:45:00" |
| LaunchSite | String | Launch facility | "CCAFS LC-40" |
| PayloadMass | Float | Payload mass in kg | 6000.0 |
| Orbit | String | Target orbit type | "LEO", "GTO", "ISS" |
| Class | Integer | Landing success (0=fail, 1=success) | 0, 1 |
| Year | Integer | Launch year (optional) | 2010, 2015 |

### Data Source

The dataset contains historical SpaceX Falcon 9 launch records including:
- Launch characteristics (site, date, flight number)
- Mission parameters (orbit, payload mass)
- Outcome data (landing success/failure)

## 🔍 Analysis Components

### 1. Data Inspection (`inspect_data`)
- Dataset dimensions and structure
- Column data types
- Missing value analysis
- Basic statistical summary
- Class distribution
- Overall success rate

### 2. Flight Pattern Analysis
- **Flight vs Payload:** How payload mass and flight number affect success
- **Flight vs Launch Site:** Launch patterns across different sites
- **Flight vs Orbit:** Evolution of orbit selection over time

### 3. Launch Site Analysis
- **Payload vs Site:** Which sites handle different payload masses
- **Site Comparison:** Success rates and launch counts by site
- Identification of site-specific constraints

### 4. Orbit Analysis
- **Success Rate by Orbit:** Which orbits have highest success rates
- **Payload vs Orbit:** Payload requirements for different orbits
- Orbit type distribution and trends

### 5. Temporal Analysis
- **Yearly Trends:** Launch frequency and success rate over time
- Evolution of landing success
- Technology improvement patterns

### 6. Correlation Analysis
- Feature correlation heatmap
- Identification of multicollinearity
- Relationship strength between variables

## 📈 Visualizations

The script generates the following visualizations:

### 1. Flight Number vs Payload Mass
- **Type:** Scatter plot with color-coded outcomes
- **Insight:** Shows learning curve and payload capability improvement
- **File:** `flight_vs_payload.png`

### 2. Flight Number vs Launch Site
- **Type:** Scatter plot by launch site
- **Insight:** Reveals site usage patterns and evolution
- **File:** `flight_vs_launchsite.png`

### 3. Payload Mass vs Launch Site
- **Type:** Scatter plot by site
- **Insight:** Identifies payload constraints per site
- **File:** `payload_vs_launchsite.png`

### 4. Success Rate by Orbit Type
- **Type:** Dual bar chart (success rate + count)
- **Insight:** Highlights most reliable orbit types
- **File:** `success_rate_by_orbit.png`

### 5. Flight Number vs Orbit Type
- **Type:** Scatter plot over time
- **Insight:** Shows orbit selection strategy evolution
- **File:** `flight_vs_orbit.png`

### 6. Payload Mass vs Orbit Type
- **Type:** Scatter plot by orbit
- **Insight:** Reveals payload-orbit relationships
- **File:** `payload_vs_orbit.png`

### 7. Yearly Trends
- **Type:** Dual line chart (launches + success rate)
- **Insight:** Demonstrates year-over-year improvements
- **File:** `yearly_trends.png`

### 8. Launch Site Comparison
- **Type:** Dual horizontal bar chart
- **Insight:** Compares site performance and utilization
- **File:** `launchsite_comparison.png`

### 9. Correlation Heatmap
- **Type:** Annotated heatmap
- **Insight:** Shows feature relationships and dependencies
- **File:** `correlation_heatmap.png`

## 🔑 Key Findings

Based on typical SpaceX launch data, the analysis reveals:

### Success Patterns
- **Flight Number Effect:** Landing success improves significantly with flight experience
- **Payload Impact:** Heavier payloads show lower success rates (physics constraint)
- **Orbit Influence:** LEO and ISS missions have higher success rates than GTO
- **Site Performance:** Some launch sites demonstrate consistently higher success rates

### Trends Over Time
- Success rate improves year-over-year (learning and technology improvements)
- Launch frequency increases as technology matures
- Transition from experimental to operational landings

### Site-Specific Insights
- VAFB-SLC shows constraints on heavy payload launches
- Different sites specialize in different orbit types
- Geographic factors influence launch capabilities

## 📁 Code Structure

```
spacex_eda_visualization.py
├── Imports and Configuration
├── Data Loading Functions
│   ├── load_data()
│   └── inspect_data()
├── Visualization Functions
│   ├── plot_flight_vs_payload()
│   ├── plot_flight_vs_launchsite()
│   ├── plot_payload_vs_launchsite()
│   ├── plot_success_rate_by_orbit()
│   ├── plot_flight_vs_orbit()
│   ├── plot_payload_vs_orbit()
│   ├── plot_yearly_trends()
│   ├── plot_launchsite_comparison()
│   └── generate_correlation_heatmap()
├── Analysis Pipeline
│   └── run_complete_eda()
└── Main Execution
    └── main()
```

## 🔧 Optimization Details

### Improvements Over Original Notebook

#### 1. **Code Organization**
- **Before:** Sequential cells in notebook
- **After:** Modular functions with clear responsibilities
- **Benefit:** Reusable, testable, maintainable code

#### 2. **Error Handling**
- Added try-catch blocks for file operations
- Graceful handling of missing columns
- Informative error messages with logging

#### 3. **Type Hints**
- All functions include type annotations
- Improves IDE support and code clarity
- Enables static type checking

#### 4. **Logging System**
- Structured logging with timestamps
- Different log levels (INFO, WARNING, ERROR)
- Helps debugging and monitoring

#### 5. **Visualization Enhancements**
- Consistent styling across all plots
- Larger, more readable fonts
- Color-coded for intuitive interpretation
- Professional publication-quality output
- Grid lines for easier reading

#### 6. **Documentation**
- Comprehensive docstrings for all functions
- Clear parameter and return type descriptions
- Usage examples and explanations

#### 7. **Configuration**
- Centralized configuration in `main()`
- Easy to modify without code changes
- Toggle figure saving on/off

#### 8. **Performance**
- Suppressed unnecessary warnings
- Efficient data operations
- Optimized plotting routines

#### 9. **Flexibility**
- Functions work independently
- Can be imported and used selectively
- Compatible with Jupyter notebooks

#### 10. **Output Quality**
- High-resolution figure saving (300 DPI)
- Summary statistics printed to console
- Key findings automatically generated

## 🐛 Troubleshooting

### Common Issues

#### 1. FileNotFoundError
```
Error: File not found: dataset_part_2.csv
```
**Solution:** Update the `DATA_FILE` path in `main()` to point to your CSV file location.

#### 2. Missing Columns
```
Warning: Year column not found. Skipping yearly trends plot.
```
**Solution:** Some plots require specific columns. The script will skip them gracefully if columns are missing.

#### 3. Import Errors
```
ModuleNotFoundError: No module named 'seaborn'
```
**Solution:** Install missing dependencies:
```bash
pip install pandas numpy matplotlib seaborn
```

#### 4. Display Issues
If plots don't display:
- Ensure you're running in an environment with display support
- For headless servers, set `save_fig=True` to save files instead
- Try adding `plt.ion()` at the beginning of script

#### 5. Memory Issues
For large datasets:
- Process data in chunks
- Generate plots one at a time
- Reduce figure resolution in `savefig(dpi=150)`

## 🔄 Workflow Integration

### Typical Data Science Pipeline

```
1. Data Collection (web scraping) ✓
2. Data Wrangling (cleaning) ✓
3. EDA (this script) ← YOU ARE HERE
4. Feature Engineering
5. Model Training
6. Model Evaluation
7. Deployment
```

### Next Steps After EDA

Based on insights from this analysis:
1. **Feature Engineering:** Create derived features (e.g., payload-to-orbit ratios)
2. **Feature Selection:** Choose most predictive features for modeling
3. **Data Preprocessing:** Scale/normalize features, encode categoricals
4. **Model Development:** Train classification models (Logistic Regression, SVM, Decision Tree, KNN)
5. **Model Evaluation:** Compare model performance and select best

## 📚 Additional Resources

### Understanding the Visualizations
- Scatter plots show individual data points and patterns
- Bar charts compare categories
- Line plots show trends over time
- Heatmaps reveal correlations

### Statistical Concepts
- **Success Rate:** Percentage of successful landings
- **Correlation:** Strength of relationship between variables (-1 to +1)
- **Distribution:** How values are spread across the range

### SpaceX Context
- **LEO:** Low Earth Orbit (easier to land from)
- **GTO:** Geostationary Transfer Orbit (harder, higher velocity)
- **ISS:** International Space Station missions
- **First Stage:** Reusable booster (main cost savings)

## 🤝 Contributing

Contributions welcome! Areas for enhancement:

- [ ] Add interactive plotly visualizations
- [ ] Implement statistical significance tests
- [ ] Add automated outlier detection
- [ ] Create HTML report generation
- [ ] Add time series decomposition
- [ ] Implement clustering analysis
- [ ] Add box plots for distributions
- [ ] Create animated visualizations

## 📝 License

This project is provided for educational purposes. Data courtesy of SpaceX and IBM.

## 🙏 Acknowledgments

- Original Jupyter Notebook from IBM Data Science course
- SpaceX for publicly available launch data
- Matplotlib and Seaborn communities for visualization tools

---

**Last Updated:** February 2026  
**Python Version:** 3.7+  
**Status:** Production Ready
