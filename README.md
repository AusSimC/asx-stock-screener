[README.md](https://github.com/user-attachments/files/25110205/README.md)
# ASX Stock Screener 📈

A web-based tool to identify buying opportunities in ASX300 stocks based on value investing principles and short interest trends.

## 🎯 What It Does

This screener ranks ASX300 stocks based on three key factors:

1. **52-Week Range Position (50% weight)** - Finds stocks trading near their lows
2. **Short Interest Trend (30% weight)** - Identifies stocks where shorts are covering
3. **P/E Ratio (20% weight)** - Focuses on value opportunities

## 🚀 Quick Start - Deploy to Streamlit Cloud (Recommended)

This is the **easiest way** to run the app - no Python installation needed!

### Step 1: Get the Code on GitHub

1. Create a free GitHub account at https://github.com (if you don't have one)
2. Create a new repository:
   - Click the "+" icon in the top right → "New repository"
   - Name it: `asx-stock-screener`
   - Make it Public
   - Click "Create repository"

3. Upload the files:
   - Click "uploading an existing file"
   - Drag and drop all these files:
     - `app.py`
     - `data_collector.py`
     - `scoring_engine.py`
     - `requirements.txt`
   - Click "Commit changes"

### Step 2: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Click "New app"
4. Fill in:
   - Repository: `your-username/asx-stock-screener`
   - Branch: `main`
   - Main file path: `app.py`
5. Click "Deploy!"

**That's it!** In 2-3 minutes, your app will be live and you'll get a public URL like:
`https://your-username-asx-stock-screener.streamlit.app`

## 💻 Alternative: Run Locally

If you want to run it on your own computer:

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Download all the files to a folder on your computer

2. Open Terminal (Mac/Linux) or Command Prompt (Windows)

3. Navigate to your folder:
   ```bash
   cd path/to/your/folder
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the app:
   ```bash
   streamlit run app.py
   ```

6. Your browser will open automatically to `http://localhost:8501`

## 📖 How to Use

1. **Click "Run Analysis"** in the sidebar to fetch the latest data
   - This takes 2-5 minutes (fetching data for 300 stocks)
   - Data is fetched fresh each time you click

2. **Review the Results**
   - Stocks are ranked by composite score (higher = better opportunity)
   - All ASX300 stocks are shown, sorted by opportunity

3. **Use Filters** (in sidebar)
   - Filter by Sector
   - Set maximum P/E ratio
   - Limit to stocks in bottom X% of 52-week range
   - Filter by short interest trend

4. **Download Results**
   - Click "Download Results as CSV" to save for further analysis

5. **Top 10 Deep Dive**
   - Expandable sections show detailed metrics for each top stock

## 📊 Understanding the Columns

- **Rank**: Overall ranking (1 = best opportunity)
- **Score**: Composite score (0-100, higher is better)
- **52w Position %**: Where current price sits in 52-week range (0% = at low, 100% = at high)
- **Short Interest (6 weeks)**: Weekly short % for last 6 weeks
- **Short Change**: Absolute change in short % (negative = declining shorts)
- **Short Trend**: Visual indicator (↓ Declining / → Stable / ↑ Increasing)

## 🔄 Data Sources

- **Stock Data**: Yahoo Finance (yfinance library)
  - Current prices
  - P/E ratios
  - Market caps
  - 52-week highs/lows
  
- **Short Interest**: ASIC Official Reports
  - URL: https://download.asic.gov.au/short-selling/
  - Updated daily (with T+4 reporting lag)
  - Percentage of shares on issue

## ⚠️ Important Notes

### Data Quality
- Yahoo Finance data can occasionally have errors or missing values
- Not all ASX300 stocks may have complete data
- Short interest data has a 4-day reporting lag

### Performance
- Initial run takes 2-5 minutes (fetching data for ~300 stocks)
- Subsequent runs are equally slow (fresh data each time)
- Consider running analysis once per day or week

### Disclaimer
**This tool is for informational and educational purposes only.**
- Not financial advice
- Past performance doesn't guarantee future results
- Always do your own research before investing
- Consult a licensed financial advisor for personalized advice

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit (Python web framework)
- **Data Collection**: yfinance, requests
- **Data Processing**: pandas, numpy

### File Structure
```
asx-stock-screener/
├── app.py              # Main Streamlit application
├── data_collector.py   # Data fetching logic
├── scoring_engine.py   # Scoring algorithm
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### Slow performance
- This is normal! Fetching data for 300 stocks takes time
- Run analysis less frequently (once per day/week)

### Missing data for some stocks
- Yahoo Finance doesn't have complete data for all stocks
- These stocks will be filtered out during scoring

### Streamlit Cloud deployment fails
- Make sure all files are uploaded to GitHub
- Check that `requirements.txt` is present
- Try redeploying from the Streamlit Cloud dashboard

## 📝 Future Enhancements (Ideas)

- Add more fundamental metrics (ROE, debt ratios, etc.)
- Include technical indicators (RSI, MACD)
- Email alerts for new opportunities
- Historical backtesting of strategy
- Watchlist functionality
- Comparison charts

## 📧 Support

If you run into issues:
1. Check this README for troubleshooting steps
2. Verify all files are in the correct location
3. Ensure you have internet connection (app needs to fetch data)

## 📄 License

This project is for personal use. Use at your own risk.

---

**Made with ❤️ for ASX investors**

Happy investing! 🚀📈
