# 🚀 GETTING STARTED - Quick Guide

## The Easiest Way to Run Your Screener

Since you mentioned you're new to Python, I recommend using **Streamlit Cloud** - it's completely free and requires zero Python installation!

---

## ✅ OPTION 1: Streamlit Cloud (RECOMMENDED - Takes 10 minutes)

### Step 1: Create GitHub Account
1. Go to https://github.com
2. Click "Sign up" (if you don't have an account)
3. Create a free account

### Step 2: Create a New Repository
1. Click the "+" icon (top right) → "New repository"
2. Repository name: `asx-stock-screener`
3. Description: "ASX stock screener for value investing"
4. Make sure "Public" is selected
5. Click "Create repository"

### Step 3: Upload Your Files
1. On the repository page, click "uploading an existing file"
2. Drag and drop these 4 files:
   - `app.py`
   - `data_collector.py`
   - `scoring_engine.py`
   - `requirements.txt`
3. Scroll down and click "Commit changes"

### Step 4: Deploy to Streamlit Cloud
1. Go to https://share.streamlit.io
2. Click "Sign in" → Sign in with GitHub
3. Click "New app"
4. Fill in the form:
   - **Repository**: Select `your-username/asx-stock-screener`
   - **Branch**: `main` (should be auto-selected)
   - **Main file path**: `app.py`
5. Click "Deploy!"

### Step 5: Wait for Deployment
- Takes 2-3 minutes
- You'll see a URL like: `https://your-username-asx-stock-screener.streamlit.app`
- Bookmark this URL!

### Step 6: Use Your Screener
1. Open your app URL
2. Click "🔄 Run Analysis" in the sidebar
3. Wait 2-5 minutes for data to load
4. Explore your results!

---

## 💻 OPTION 2: Run on Your Computer (If You Want)

### Step 1: Install Python
1. Go to https://www.python.org/downloads/
2. Download Python 3.12 (or latest)
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Install

### Step 2: Open Terminal/Command Prompt
- **Mac**: Open "Terminal" app
- **Windows**: Open "Command Prompt" or "PowerShell"

### Step 3: Navigate to Your Files
```bash
cd Desktop/asx-screener
```
(Replace with wherever you saved the files)

### Step 4: Install Dependencies
```bash
pip install streamlit pandas yfinance numpy requests
```

### Step 5: Run the App
```bash
streamlit run app.py
```

Your browser will open automatically!

---

## 🎯 How to Actually Use the Screener

### First Time:
1. Open the app
2. Read the "How This Works" section (click to expand)
3. Click "🔄 Run Analysis" button (sidebar)
4. **Go make a coffee** ☕ - takes 2-5 minutes
5. Results appear!

### Understanding Results:
- **Rank 1-10**: Best opportunities (lowest in 52w range + declining shorts + low P/E)
- **Score**: Higher = better opportunity
- **52w Position %**: Lower = closer to 52-week low
- **Short Change**: Negative = shorts are covering (good sign!)
- **Short Trend**: ↓ = Declining (what you want to see)

### Using Filters (Sidebar):
- **Sector**: Focus on specific sectors
- **Max P/E**: Filter out expensive stocks
- **Max 52w Position**: Only show stocks in bottom X% of range
- **Short Trend**: Only show declining/stable shorts

### What to Do with Results:
1. Focus on Rank 1-20 stocks
2. Look for: Low 52w position % + Declining shorts + Low P/E
3. Click the expander to see detailed metrics
4. **Do your own research** on the companies
5. Check their latest announcements on ASX website
6. Make informed decisions!

---

## 🔄 How Often to Run

- **Daily**: If you're actively trading
- **Weekly**: For longer-term investing (recommended)
- **When you hear news**: Re-run to see updated positions

Each time you click "Run Analysis" it fetches fresh data.

---

## ⚠️ IMPORTANT REMINDERS

1. **Not Financial Advice**: This is a screening tool, not advice
2. **Do Your Research**: Always investigate companies before buying
3. **Data Lag**: Short interest has 4-day delay
4. **Diversify**: Don't put all eggs in one basket
5. **Risk Management**: Only invest what you can afford to lose

---

## 🆘 Troubleshooting

### Streamlit Cloud - "App is starting..."
- Wait 2-3 minutes on first deploy
- Refresh the page

### "Module not found" error (local install)
```bash
pip install streamlit pandas yfinance numpy requests
```

### Slow performance
- Normal! Fetching 300 stocks takes time
- Be patient during "Run Analysis"

### Some stocks missing
- Yahoo Finance doesn't have data for all stocks
- This is normal and expected

---

## 📞 Need Help?

If something isn't working:

1. **Check this guide again** - did you follow all steps?
2. **Try Streamlit Cloud** - easiest option, fewer things to go wrong
3. **Check your internet** - app needs internet to fetch data
4. **Wait longer** - data collection takes 2-5 minutes

---

## 🎉 You're All Set!

You now have a professional-grade stock screener that:
- ✅ Analyzes all ASX300 stocks
- ✅ Tracks short interest trends
- ✅ Ranks by your custom criteria
- ✅ Updates on-demand with fresh data

**Good luck with your investing!** 📈🚀

Remember: The screener finds opportunities, but YOU make the final decisions!
