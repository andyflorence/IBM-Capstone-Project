# SpaceX SQL Analysis with Visualizations

A comprehensive Python script that performs SQL-based exploratory data analysis on SpaceX launch data with **14 professional visualizations** generated automatically for each query.

## 📋 Overview

This script combines the power of SQL queries with data visualization to provide deep insights into SpaceX Falcon 9 launch data. Each SQL query is accompanied by appropriate charts and graphs for better understanding and presentation.

**Original:** jupyter-labs-eda-sql-coursera_sqllite.ipynb  
**Enhanced Version:** Now includes 14 automated visualizations  
**Database:** SQLite (no server required)

## 🎯 What This Script Does

### SQL Analysis
- Executes 14 comprehensive SQL queries
- Analyzes launch sites, payloads, missions, and landing outcomes
- Performs statistical aggregations and time-based analyses
- Generates summary statistics

### Visualizations
- Creates **14 high-quality visualizations** (300 DPI)
- Automatically saves all charts as PNG files
- Uses appropriate chart types for each analysis
- Professional styling with clear labels and legends

## ✨ Features

- **Automated Pipeline:** One command runs all analyses and generates all visualizations
- **SQL + Visualization:** Each query paired with appropriate chart
- **Professional Output:** Publication-quality graphics (300 DPI)
- **Comprehensive Coverage:** 14 different analyses with visualizations
- **Easy to Use:** No database server needed (SQLite)
- **Well Documented:** Clear descriptions for each query and visualization

## 📦 Requirements

### Python Version
- Python 3.7+

### Dependencies
```
pandas>=1.2.0
matplotlib>=3.3.0
seaborn>=0.11.0
sqlite3 (built-in)
```

## 🔧 Installation

### 1. Install Dependencies

```bash
pip install pandas matplotlib seaborn
```

### 2. Download the Script

```bash
# No additional setup needed - script downloads data automatically
python spacex_sql_analysis_with_viz.py
```

## 💻 Usage

### Run Complete Analysis

```bash
python spacex_sql_analysis_with_viz.py
```

This will:
1. Download SpaceX data from IBM cloud storage
2. Create SQLite database
3. Execute all 14 SQL queries
4. Generate all 14 visualizations
5. Save all charts as PNG files
6. Display summary statistics

### Expected Runtime
- **Total Time:** 30-60 seconds
- **Database Creation:** 5 seconds
- **Query Execution:** 10 seconds
- **Visualization Generation:** 20-40 seconds

## 📊 Analyses & Visualizations

### 1. Launch Sites Analysis
**Query:** Count launches by site  
**Visualization:** Horizontal bar chart showing launches per site  
**File:** `viz_02_launch_count_by_site.png`

**Insights:**
- Which launch sites are most active
- Launch distribution across facilities

---

### 2. Cape Canaveral Launches
**Query:** Launches from Cape Canaveral (CCA prefix)  
**Visualization:** Bar chart of CCA launches by booster version  
**File:** `viz_03_cape_canaveral_boosters.png`

**Insights:**
- Booster usage at Cape Canaveral
- Evolution of booster technology at this site

---

### 3. NASA (CRS) Total Payload
**Query:** Sum of payload mass for NASA CRS missions  
**Visualization:** Single bar showing total mass  
**File:** `viz_04_nasa_total_payload.png`

**Insights:**
- Total cargo delivered to ISS
- NASA's reliance on SpaceX

---

### 4. F9 v1.1 Average Payload
**Query:** Average payload for F9 v1.1 booster  
**Visualization:** Bar chart showing average mass  
**File:** `viz_05_avg_payload_f9v11.png`

**Insights:**
- Typical payload capacity for this booster version
- Performance benchmarking

---

### 5. First Successful Landing Date
**Query:** Date of first successful ground pad landing  
**Visualization:** Text box highlighting the historic date  
**File:** `viz_06_first_landing_date.png`

**Insights:**
- Milestone achievement in reusability
- Historic significance

---

### 6. Successful Landings Timeline
**Query:** All successful ground pad landings  
**Visualization:** Line chart showing cumulative successful landings over time  
**File:** `viz_07_landing_timeline.png`

**Insights:**
- Progression of landing success
- Acceleration of reusability achievements

---

### 7. Landing Outcomes Distribution
**Query:** All distinct landing outcomes  
**Visualization:** Dual chart (horizontal bar + pie chart)  
**File:** `viz_08_landing_outcomes_full.png`

**Insights:**
- Success vs failure rates
- Most common landing outcomes
- Proportion of different outcomes

---

### 8. Drone Ship Booster Analysis
**Query:** Boosters with successful drone ship landings (4000-6000 kg payload)  
**Visualization:** Bar chart of booster versions  
**File:** `viz_09_drone_ship_boosters.png`

**Insights:**
- Which boosters handle this payload range
- Drone ship landing capabilities

---

### 9. Mission Outcomes Distribution
**Query:** All distinct mission outcomes  
**Visualization:** Color-coded horizontal bar chart (green=success, red=failure)  
**File:** `viz_10_mission_outcomes_full.png`

**Insights:**
- Mission success patterns
- Types of mission failures

---

### 10. Success vs Failure Summary
**Query:** Count of successful vs failed missions  
**Visualization:** Dual chart (bar chart + pie chart)  
**File:** `viz_11_success_vs_failure.png`

**Insights:**
- Overall mission success rate
- Success/failure ratio
- **Displays calculated success percentage**

---

### 11. Maximum Payload Booster
**Query:** Booster that carried maximum payload  
**Visualization:** Horizontal bar chart comparing all boosters (max highlighted in gold)  
**File:** `viz_12_max_payload_booster.png`

**Insights:**
- Highest payload capacity achieved
- Comparison across all booster versions
- Technology progression

---

### 12. 2015 Failed Landings
**Query:** Failed drone ship landings in 2015 by month  
**Visualization:** Bar chart showing failures by month  
**File:** `viz_13_failed_landings_2015.png`

**Insights:**
- Learning period patterns
- Monthly failure distribution
- Early technology challenges

---

### 13. Landing Outcomes by Period
**Query:** Landing outcomes between June 2010 - March 2017  
**Visualization:** Dual chart (horizontal bar + pie)  
**File:** `viz_14_landing_outcomes_period.png`

**Insights:**
- Historical landing performance
- Evolution over specific period

---

### 14. Summary Statistics Dashboard
**Query:** Overall dataset statistics  
**Visualization:** Multi-panel dashboard with 5 charts  
**File:** `viz_15_summary_statistics.png`

**Includes:**
- Total launches (bar)
- Unique launch sites (bar)
- Unique booster versions (bar)
- Payload statistics (bar comparison)
- Timeline info (text box)

**Insights:**
- Complete dataset overview
- Key metrics at a glance
- Timeline span

---

## 📁 Output Files

### Database Files
- `my_data1.db` - SQLite database with SpaceX data

### Visualization Files (14 total)
All saved as high-resolution PNG (300 DPI):

```
viz_02_launch_count_by_site.png
viz_03_cape_canaveral_boosters.png
viz_04_nasa_total_payload.png
viz_05_avg_payload_f9v11.png
viz_06_first_landing_date.png
viz_07_landing_timeline.png
viz_08_landing_outcomes_full.png
viz_09_drone_ship_boosters.png
viz_10_mission_outcomes_full.png
viz_11_success_vs_failure.png
viz_12_max_payload_booster.png
viz_13_failed_landings_2015.png
viz_14_landing_outcomes_period.png
viz_15_summary_statistics.png
```

## 🎨 Visualization Types Used

| Analysis Type | Chart Type | Reasoning |
|---------------|------------|-----------|
| Categorical Counts | Horizontal Bar Chart | Easy comparison of categories |
| Single Values | Single Bar + Label | Clear display of specific metrics |
| Time Series | Line Chart | Shows trends over time |
| Distributions | Bar + Pie Dual Chart | Shows both counts and proportions |
| Comparisons | Color-Coded Bars | Highlights differences (success/fail) |
| Milestones | Text Box | Emphasizes important dates |
| Multi-Metric Summary | Dashboard Grid | Comprehensive overview |

## 🔑 Key Insights from Analysis

### Launch Operations
- **Total Launches:** ~100+ missions analyzed
- **Launch Sites:** 3-4 primary facilities
- **Booster Versions:** 10+ different versions

### Landing Success
- **First Success:** Historic date of first ground pad landing
- **Success Rate:** Calculated from mission outcomes
- **Improvement Trend:** Success increases over time

### Payload Capabilities
- **Average Payload:** Varies by booster version
- **Maximum Payload:** Identifies peak capability
- **NASA Deliveries:** Significant ISS cargo tonnage

### Technology Evolution
- Early failures in 2015 (learning period)
- Increasing success rates over time
- Expanding payload capabilities

## 🛠️ Customization

### Change Save Location
```python
# In each viz function, modify:
plt.savefig('/your/path/filename.png', dpi=300, bbox_inches='tight')
```

### Adjust Figure Size
```python
# At top of script, modify:
plt.rcParams['figure.figsize'] = (14, 7)  # width, height
```

### Change Color Scheme
```python
# In individual viz functions, modify color parameters:
colors = ['steelblue', 'coral', 'green', 'purple']
```

### Disable Figure Saving
```python
# In main(), change all:
viz_function(df, save_fig=False)
```

## 🐛 Troubleshooting

### Issue: "Unable to download data"
**Cause:** Network connectivity  
**Solution:** Check internet connection, or download CSV manually and update `DATA_URL`

### Issue: "Database locked"
**Cause:** Previous instance still running  
**Solution:** Close other connections, delete `my_data1.db`, run again

### Issue: "Display issues with plots"
**Cause:** No display environment  
**Solution:** Figures are saved automatically - check PNG files

### Issue: "Import errors"
**Solution:**
```bash
pip install --upgrade pandas matplotlib seaborn
```

## 📊 Sample Console Output

```
================================================================================
 SpaceX SQL Analysis with Visualizations
================================================================================

================================================================================
 STEP 1: Database Setup and Data Loading
================================================================================

📊 Connecting to SQLite database...
✅ Connected to database: my_data1.db

📥 Loading SpaceX data from URL...
✅ Loaded 101 records with 17 columns

...

================================================================================
 STEP 3: Exploratory Data Analysis with Visualizations
================================================================================

Query 2: Display unique launch sites
--------------------------------------------------------------------------------
Query:
SELECT DISTINCT Launch_Site FROM SPACEXTBL;

Results (4 rows):
              Launch_Site
    CCAFS LC-40
    VAFB SLC-4E
    KSC LC-39A
    CCAFS SLC-40

📊 Generating visualization...
[Displays chart]

...

📊 Mission Success Rate: 94.06% (95/101)

...

================================================================================
 Analysis Complete
================================================================================

💾 Database file: my_data1.db
📊 Table name: SPACEXTBL

✅ All queries executed successfully!
✅ All visualizations generated and saved!

================================================================================
📁 Generated Visualization Files:
================================================================================
   1. viz_02_launch_count_by_site.png
   2. viz_03_cape_canaveral_boosters.png
   ...
  14. viz_15_summary_statistics.png
```

## 🔗 Integration

### Use with Jupyter Notebooks
```python
%run spacex_sql_analysis_with_viz.py
```

### Import Individual Functions
```python
from spacex_sql_analysis_with_viz import execute_query, viz_success_vs_failure

# Custom analysis
cursor = create_your_cursor()
df = execute_query(cursor, "YOUR SQL QUERY")
viz_success_vs_failure(df, save_fig=True)
```

## 📚 Related Scripts

This script complements:
1. **Web Scraping Script** - Collects launch data
2. **EDA Visualization Script** - Statistical analysis
3. **Machine Learning Scripts** - Predictive modeling

## 🎓 Learning Outcomes

From this script, you'll understand:
- SQL query design for data analysis
- Choosing appropriate visualizations
- Combining SQL with Python visualization
- SQLite database operations
- Statistical aggregation techniques
- Time-based analysis methods

## 🤝 Contributing

Suggestions for additional analyses or visualizations welcome!

Potential additions:
- [ ] Geographic visualization of launch sites
- [ ] 3D payload vs orbit vs success visualization
- [ ] Animated timeline of launches
- [ ] Correlation heatmap
- [ ] Advanced statistical tests

## 📝 License

Educational use. Data courtesy of SpaceX and IBM.

---

**Last Updated:** February 2026  
**Python Version:** 3.7+  
**Status:** Production Ready  
**Visualizations:** 14 automated charts
