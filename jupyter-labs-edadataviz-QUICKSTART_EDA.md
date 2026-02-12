# Quick Reference Guide - SpaceX EDA Script

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_eda.txt
```

### 2. Update Data Path
Edit `spacex_eda_visualization.py`:
```python
DATA_FILE = "your_data_file.csv"  # Line 591
```

### 3. Run Analysis
```bash
python spacex_eda_visualization.py
```

## 📊 What You'll Get

### Console Output
- Dataset overview (shape, columns, types)
- Missing value report
- Basic statistics
- Class distribution and success rate
- Orbit success rate summary
- Launch site summary
- Key findings summary

### Visualizations (9 plots)
1. **flight_vs_payload.png** - Learning curve analysis
2. **flight_vs_launchsite.png** - Site usage patterns
3. **payload_vs_launchsite.png** - Site payload constraints
4. **success_rate_by_orbit.png** - Orbit reliability comparison
5. **flight_vs_orbit.png** - Orbit selection evolution
6. **payload_vs_orbit.png** - Payload-orbit relationships
7. **yearly_trends.png** - Temporal improvement patterns
8. **launchsite_comparison.png** - Site performance comparison
9. **correlation_heatmap.png** - Feature relationships

## 🔧 Common Customizations

### Don't Save Figures
```python
SAVE_FIGURES = False  # Line 592 in main()
```

### Run Specific Analyses
```python
from spacex_eda_visualization import *

df = load_data("data.csv")
plot_success_rate_by_orbit(df, save_fig=True)
plot_launchsite_comparison(df, save_fig=True)
```

### Change Figure Size
```python
plt.rcParams['figure.figsize'] = (16, 8)  # Line 30
```

### Adjust Color Scheme
Modify in individual plot functions:
```python
palette={0: 'red', 1: 'green'}  # Change colors
```

## 📋 Expected Data Format

### Required Columns
- `FlightNumber` (int) - Sequential flight number
- `LaunchSite` (str) - Launch facility name
- `PayloadMass` (float) - Payload mass in kg
- `Orbit` (str) - Target orbit type
- `Class` (int) - Landing outcome (0=fail, 1=success)

### Optional Columns
- `Year` (int) - For yearly trend analysis
- `Date` (str/date) - For temporal analysis
- `Time` (str/time) - Launch time

### Example Data
```csv
FlightNumber,LaunchSite,PayloadMass,Orbit,Class,Year
1,CCAFS LC-40,6000,LEO,0,2010
2,CCAFS LC-40,8500,ISS,0,2010
3,VAFB SLC-4E,500,LEO,1,2013
```

## 🎯 Analysis Workflow

### 1. Data Inspection
```python
df = load_data("data.csv")
inspect_data(df)  # Comprehensive overview
```

### 2. Individual Visualizations
```python
# Flight patterns
plot_flight_vs_payload(df)
plot_flight_vs_launchsite(df)
plot_flight_vs_orbit(df)

# Site analysis
plot_payload_vs_launchsite(df)
plot_launchsite_comparison(df)

# Orbit analysis
plot_success_rate_by_orbit(df)
plot_payload_vs_orbit(df)

# Trends
plot_yearly_trends(df)

# Correlations
generate_correlation_heatmap(df)
```

### 3. Complete Pipeline
```python
df = run_complete_eda("data.csv", save_figures=True)
```

## 💡 Interpretation Tips

### Success Rate Colors
- 🟢 Green points = Successful landing (Class=1)
- 🔴 Red points = Failed landing (Class=0)

### Reading Scatter Plots
- **Clusters:** Groups of similar outcomes
- **Trends:** Upward/downward patterns
- **Outliers:** Unusual data points

### Reading Bar Charts
- **Higher bars:** Better success rate or more launches
- **Color intensity:** Success rate indicator (green=high)

### Reading Heatmaps
- **Red:** Positive correlation
- **Blue:** Negative correlation
- **White/Gray:** No correlation

## 🔍 Key Insights to Look For

### Flight Number Analysis
- Does success improve with more flights?
- Are early flights riskier?

### Payload Analysis
- Do heavier payloads correlate with failures?
- What's the optimal payload range?

### Orbit Analysis
- Which orbits are most reliable?
- Are certain orbits never attempted?

### Site Analysis
- Do some sites outperform others?
- Are there site-specific constraints?

### Temporal Analysis
- Is success rate improving over time?
- Are launch frequencies increasing?

## ⚠️ Common Issues

### Issue: "File not found"
**Fix:** Update `DATA_FILE` path to absolute path
```python
DATA_FILE = "/full/path/to/dataset_part_2.csv"
```

### Issue: "Year column not found"
**Effect:** Yearly trends plot skipped
**Fix:** Add Year column to dataset or skip that analysis

### Issue: Plots not displaying
**Fix 1:** Run in Jupyter notebook with `%matplotlib inline`
**Fix 2:** Set `SAVE_FIGURES = True` to save to files
**Fix 3:** Add `plt.show()` if needed

### Issue: ImportError
**Fix:** Install missing package
```bash
pip install <package-name>
```

## 📈 Performance Tips

### For Large Datasets
- Sample data for quick exploration: `df.sample(n=1000)`
- Reduce figure resolution: `dpi=150` instead of `dpi=300`
- Generate plots one at a time instead of full pipeline

### For Better Performance
- Close figures after viewing: `plt.close('all')`
- Use `.head()` for quick checks
- Comment out plots you don't need

## 🎨 Customization Examples

### Change Plot Style
```python
sns.set_style("darkgrid")  # or "whitegrid", "dark", "white", "ticks"
```

### Adjust Font Sizes
```python
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
```

### Custom Color Palette
```python
custom_colors = {'0': '#FF6B6B', '1': '#4ECDC4'}
sns.scatterplot(..., palette=custom_colors)
```

## 🔗 Integration with Other Scripts

### After Web Scraping
```python
# Use output from web scraping script
df = load_data("spacex_launches.csv")
```

### Before Modeling
```python
# Export cleaned data for modeling
df.to_csv("cleaned_data_for_modeling.csv", index=False)
```

### With Jupyter Notebooks
```python
# In notebook cell
%run spacex_eda_visualization.py
```

## 📚 Function Reference

### Data Functions
- `load_data(filepath)` - Load CSV file
- `inspect_data(df)` - Display data overview

### Plot Functions
- `plot_flight_vs_payload(df, save_fig)` - Flight-payload relationship
- `plot_flight_vs_launchsite(df, save_fig)` - Flight-site patterns
- `plot_payload_vs_launchsite(df, save_fig)` - Payload-site constraints
- `plot_success_rate_by_orbit(df, save_fig)` - Orbit success comparison
- `plot_flight_vs_orbit(df, save_fig)` - Flight-orbit evolution
- `plot_payload_vs_orbit(df, save_fig)` - Payload-orbit relationships
- `plot_yearly_trends(df, save_fig)` - Year-over-year trends
- `plot_launchsite_comparison(df, save_fig)` - Site performance
- `generate_correlation_heatmap(df, save_fig)` - Feature correlations

### Pipeline Function
- `run_complete_eda(filepath, save_figures)` - Complete analysis

---

**Need Help?** Check the full README_EDA.md for detailed documentation!
