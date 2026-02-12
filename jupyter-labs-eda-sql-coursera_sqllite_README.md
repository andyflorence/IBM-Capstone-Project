# SpaceX SQL Analysis - Python Scripts

## Overview

This repository contains Python scripts converted from the Jupyter notebook `jupyter-labs-eda-sql-coursera_sqllite.ipynb`. The scripts perform exploratory data analysis on SpaceX launch data using SQL queries.

## 📁 Files

### 1. `spacex_sql_analysis.py`
**Full-featured version** with detailed documentation and comprehensive output.

**Features:**
- Detailed section headers and query descriptions
- Step-by-step execution flow
- Comprehensive error handling
- Summary statistics
- Formatted DataFrame output

**Best for:** Learning, documentation, detailed analysis

### 2. `spacex_sql_analysis_simple.py`
**Streamlined version** with cleaner code and modular design.

**Features:**
- Dictionary-based query management
- Reusable utility functions
- Clean, concise output
- Easy to extend with new queries

**Best for:** Production use, integration into larger projects, quick analysis

## 🚀 Quick Start

### Prerequisites

```bash
pip install pandas
```

Note: `sqlite3` is included in Python standard library

### Running the Analysis

**Option 1: Full version**
```bash
python spacex_sql_analysis.py
```

**Option 2: Simple version**
```bash
python spacex_sql_analysis_simple.py
```

## 📊 Analysis Performed

The scripts execute 14 SQL queries analyzing:

### 1. **Data Exploration**
- Table schema and structure
- Unique launch sites
- Distinct landing outcomes
- Distinct mission outcomes

### 2. **Launch Site Analysis**
- All unique launch sites
- Launches from Cape Canaveral (CCA)

### 3. **Payload Analysis**
- Total payload mass for NASA (CRS) missions
- Average payload mass for F9 v1.1 booster
- Booster versions carrying maximum payload

### 4. **Landing Outcome Analysis**
- First successful ground pad landing date
- All successful ground pad landings (chronological)
- Booster versions with successful drone ship landings (specific payload range)
- Failed drone ship landings in 2015
- Landing outcome distribution (2010-2017)

### 5. **Mission Success Analysis**
- Count of successful vs failed missions
- Mission outcome distribution

### 6. **Summary Statistics**
- Total launches
- Unique launch sites and booster types
- Date range (first to last launch)
- Average and maximum payload mass

## 📝 Sample Output

```
================================================================================
 Query 1/14: Unique Launch Sites
================================================================================

SELECT DISTINCT Launch_Site FROM SPACEXTBL;

✅ Results (4 rows):
                      Launch_Site
         CCAFS LC-40
         VAFB SLC-4E
         KSC LC-39A
         CCAFS SLC-40

================================================================================
 Query 2/14: Total Payload Mass for NASA (CRS)
================================================================================

SELECT SUM(PAYLOAD_MASS__KG_) AS TOTAL_PAYLOAD_MASS_KG
FROM SPACEXTBL
WHERE CUSTOMER = 'NASA (CRS)';

✅ Results (1 rows):
   TOTAL_PAYLOAD_MASS_KG
                45596.0
```

## 🗄️ Database Structure

**Database:** `my_data1.db` (SQLite)

**Tables:**
- `SPACEXTBL` - Main data table (loaded from CSV)
- `SPACEXTABLE` - Cleaned table (null dates removed)

**Key Columns:**
- `Date` - Launch date
- `Launch_Site` - Launch location
- `Booster_Version` - Type of booster used
- `PAYLOAD_MASS__KG_` - Payload mass in kilograms
- `Customer` - Customer name
- `Mission_Outcome` - Mission success/failure
- `Landing_Outcome` - Landing success/failure/type

## 🔧 Customization

### Adding New Queries

**For the simple version**, add to the `QUERIES` dictionary:

```python
QUERIES = {
    # ... existing queries ...
    
    'your_query_name': {
        'description': 'Your Query Description',
        'sql': """
            SELECT *
            FROM SPACEXTBL
            WHERE your_condition;
        """
    }
}
```

### Changing Data Source

Modify the `CONFIG` dictionary (simple version) or `DATA_URL` constant (full version):

```python
CONFIG = {
    'database': 'your_database.db',
    'table': 'YOUR_TABLE',
    'data_url': 'https://your-data-source.com/data.csv'
}
```

## 📋 Query Reference

| # | Query Name | Description |
|---|------------|-------------|
| 1 | Schema | Display table structure |
| 2 | Launch Sites | List all unique launch sites |
| 3 | CCA Launches | First 5 launches from Cape Canaveral |
| 4 | NASA Payload | Total payload for NASA (CRS) |
| 5 | F9 Avg Payload | Average payload for F9 v1.1 |
| 6 | First Ground Landing | Date of first successful ground pad landing |
| 7 | All Ground Landings | All successful ground pad landings |
| 8 | Landing Outcomes | All distinct landing outcomes |
| 9 | Drone Ship Boosters | Boosters with successful drone landings (4-6t) |
| 10 | Mission Outcomes | All distinct mission outcomes |
| 11 | Success Rate | Count of successful vs failed missions |
| 12 | Max Payload Booster | Booster that carried maximum payload |
| 13 | Failed 2015 | Failed drone ship landings in 2015 |
| 14 | Outcome Distribution | Landing outcomes by count (2010-2017) |

## 🎯 Key Insights from the Analysis

Based on the queries, you can discover:

1. **Launch Infrastructure**: SpaceX uses 4 main launch sites
2. **Payload Capability**: Maximum payload capacity and average loads
3. **Landing Success**: Success rates for different landing types
4. **Booster Evolution**: How different booster versions performed
5. **Customer Distribution**: Which customers use SpaceX services
6. **Timeline**: Evolution of SpaceX launches from 2010-2017

## 🐛 Troubleshooting

### Connection Error
```
Error: unable to open database file
```
**Solution:** Ensure you have write permissions in the current directory

### Data Loading Error
```
Error loading data: HTTPError
```
**Solution:** Check your internet connection or verify the data URL

### Query Error
```
Error executing query: no such column
```
**Solution:** Run `PRAGMA table_info(SPACEXTBL)` to verify column names

## 📚 Learning Resources

- **Original Notebook**: Coursera IBM Data Science Capstone
- **SQLite Documentation**: https://www.sqlite.org/docs.html
- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **SQL Tutorial**: https://www.w3schools.com/sql/

## 🤝 Contributing

To add new queries or improve the analysis:

1. Fork the repository
2. Add your query to the appropriate section
3. Test thoroughly
4. Submit a pull request

## 📄 License

This project is based on IBM Coursera content.

**Original Authors:**
- Lakshmi Holla
- Rav Ahuja

**Converted to Python:** 2026-02-10

## 🙏 Acknowledgments

- IBM Data Science Course on Coursera
- SpaceX for making launch data publicly available
- Skills Network for providing the dataset

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the original Jupyter notebook
3. Consult SQL/Python documentation

---

**Note:** These scripts are educational tools for learning SQL and data analysis with Python. The data represents SpaceX launches from 2010-2017 and may not reflect current launch statistics.
