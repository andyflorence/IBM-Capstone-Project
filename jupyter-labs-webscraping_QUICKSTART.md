# Quick Start Guide - SpaceX Launch Scraper

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install beautifulsoup4 requests pandas
```

### Step 2: Run the Script
```bash
python spacex_launch_scraper.py
```

### Step 3: View Results
The script will create `spacex_launches.csv` with all the launch data!

## 📊 What You'll Get

The script extracts the following data for each SpaceX launch:

- Flight number
- Launch date and time
- Booster version
- Launch site
- Payload name and mass
- Target orbit
- Customer
- Launch outcome
- Booster landing status

## 🎯 Example Output

```
================================================================================
SPACEX LAUNCH DATA EXTRACTION SUMMARY
================================================================================

Total records extracted: 121
Columns: Flight No., Date, Time, Version Booster, Launch site, Payload, ...

First 5 records:
   Flight No.          Date   Time  Version Booster    Launch site  ...
0           1  4 June 2010  18:45  F9 v1.0B0003.1   CCAFS SLC-40  ...
1           2  8 December 2010  15:43  F9 v1.0B0004.1   CCAFS SLC-40  ...
...
```

## 💡 Tips

1. **Network Required**: The script needs internet to fetch Wikipedia
2. **Static Snapshot**: Data is from June 9, 2021
3. **Output Location**: Look for `spacex_launches.csv` in the same directory
4. **Logs**: Check console output for detailed progress information

## 🔧 Troubleshooting

### ModuleNotFoundError
```bash
# Install missing packages
pip install beautifulsoup4 requests pandas
```

### Connection Error
- Check your internet connection
- Verify Wikipedia is accessible
- Script uses a static URL snapshot, so it should be stable

### No Data Extracted
- Check the log messages for specific errors
- Verify Wikipedia's HTML structure hasn't changed (unlikely with static URL)

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed information
- Check [CODE_REVIEW.md](CODE_REVIEW.md) for optimization details
- Explore the CSV file with pandas, Excel, or your favorite data tool

## 🎓 Use Cases

This data is perfect for:
- Machine learning models (predicting landing success)
- Data visualization projects
- Statistical analysis of SpaceX launches
- Educational projects on web scraping
- Time series analysis of launch frequency

---

Happy scraping! 🚀
