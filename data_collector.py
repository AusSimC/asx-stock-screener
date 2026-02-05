"""
ASX Stock Screener - Data Collection Module
Fetches stock data from Yahoo Finance and ASIC short interest data
"""

import pandas as pd
import yfinance as yf
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import time

# Import the extended ASX300 ticker list
try:
    from asx300_tickers import ASX300_TICKERS_EXTENDED
    ASX300_TICKERS = ASX300_TICKERS_EXTENDED
except ImportError:
    # Fallback to a smaller list if the extended list file isn't available
    ASX300_TICKERS = [
        'BHP.AX', 'CBA.AX', 'CSL.AX', 'NAB.AX', 'WBC.AX', 'ANZ.AX', 'WES.AX', 'MQG.AX',
        'FMG.AX', 'WDS.AX', 'RIO.AX', 'WOW.AX', 'GMG.AX', 'TCL.AX', 'TLS.AX', 'REA.AX',
        'COL.AX', 'ALL.AX', 'STO.AX', 'QBE.AX', 'WTC.AX', 'S32.AX', 'RMD.AX', 'IAG.AX',
        'AMP.AX', 'ORG.AX', 'AGL.AX', 'SUN.AX', 'JHX.AX', 'CPU.AX'
    ]

def get_asic_short_data(weeks: int = 6) -> pd.DataFrame:
    """
    Fetch ASIC short interest data for the last N weeks
    Returns DataFrame with ticker, date, short_positions, short_pct
    """
    print(f"Fetching ASIC short interest data for last {weeks} weeks...")
    
    all_data = []
    today = datetime.now()
    
    # Get data for last N weeks (going back day by day to capture weekly snapshots)
    for days_back in range(0, weeks * 7, 7):  # Check weekly
        target_date = today - timedelta(days=days_back)
        date_str = target_date.strftime('%Y%m%d')
        
        url = f"https://download.asic.gov.au/short-selling/RR{date_str}-001-SSDailyYTD.csv"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Parse the CSV - it has a complex header structure
                lines = response.text.strip().split('\n')
                
                # Find the header row (contains "Product,Product Code")
                header_idx = None
                for i, line in enumerate(lines):
                    if line.startswith('Product,Product Code'):
                        header_idx = i
                        break
                
                if header_idx is not None:
                    # Get the dates from first row
                    date_row = lines[0].split(',')
                    # Get the most recent date column (usually first data column after Product Code)
                    
                    # Parse data rows
                    data_lines = lines[header_idx+1:]
                    for line in data_lines:
                        parts = line.split(',')
                        if len(parts) >= 4:
                            company_name = parts[0]
                            ticker = parts[1]
                            short_positions = parts[2]
                            short_pct = parts[3]
                            
                            # Only keep if we have valid data
                            if short_positions and short_positions != '-':
                                all_data.append({
                                    'date': target_date.strftime('%Y-%m-%d'),
                                    'ticker': ticker,
                                    'company_name': company_name,
                                    'short_positions': short_positions,
                                    'short_pct': float(short_pct) if short_pct and short_pct != '-' else 0.0
                                })
                
                print(f"  ✓ Retrieved data for {target_date.strftime('%Y-%m-%d')}")
            else:
                print(f"  ✗ No data for {target_date.strftime('%Y-%m-%d')}")
        except Exception as e:
            print(f"  ✗ Error fetching {date_str}: {str(e)}")
        
        time.sleep(0.5)  # Be nice to ASIC servers
    
    df = pd.DataFrame(all_data)
    print(f"Total records fetched: {len(df)}")
    return df


def get_stock_data(ticker: str) -> Dict:
    """
    Fetch stock data from Yahoo Finance for a single ticker
    Returns dict with all relevant metrics
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="1y")
        
        if hist.empty or len(hist) < 2:
            return None
        
        # Calculate current position in 52-week range
        current_price = hist['Close'].iloc[-1]
        week52_high = hist['High'].max()
        week52_low = hist['Low'].min()
        
        if week52_high > week52_low:
            range_position = ((current_price - week52_low) / (week52_high - week52_low)) * 100
        else:
            range_position = 50.0  # Default if no range
        
        # Get sector
        sector = info.get('sector', 'Unknown')
        
        # Get P/E ratio
        pe_ratio = info.get('trailingPE', info.get('forwardPE', None))
        
        # Get market cap
        market_cap = info.get('marketCap', 0)
        
        return {
            'ticker': ticker,
            'company_name': info.get('longName', info.get('shortName', ticker)),
            'sector': sector,
            'current_price': round(current_price, 2),
            'market_cap': market_cap,
            'pe_ratio': round(pe_ratio, 2) if pe_ratio and pe_ratio > 0 else None,
            'week52_high': round(week52_high, 2),
            'week52_low': round(week52_low, 2),
            'range_position_pct': round(range_position, 1)
        }
    
    except Exception as e:
        print(f"Error fetching {ticker}: {str(e)}")
        return None


def calculate_short_interest_metrics(short_df: pd.DataFrame, ticker_base: str) -> Dict:
    """
    Calculate 6-week short interest trend for a ticker
    ticker_base should be without .AX suffix (e.g., 'BHP' not 'BHP.AX')
    """
    # Filter for this ticker
    ticker_data = short_df[short_df['ticker'] == ticker_base].copy()
    
    if ticker_data.empty:
        return {
            'short_history': [],
            'absolute_change': None,
            'trend': 'No Data'
        }
    
    # Sort by date
    ticker_data = ticker_data.sort_values('date')
    
    # Get last 6 weeks (or however many we have)
    recent = ticker_data.tail(6)
    
    short_history = []
    for _, row in recent.iterrows():
        short_history.append({
            'date': row['date'],
            'short_pct': row['short_pct']
        })
    
    # Calculate absolute change (most recent - oldest in our dataset)
    if len(short_history) >= 2:
        absolute_change = short_history[-1]['short_pct'] - short_history[0]['short_pct']
        
        if absolute_change < -0.1:  # Declining by more than 0.1%
            trend = '↓ Declining'
        elif absolute_change > 0.1:  # Increasing by more than 0.1%
            trend = '↑ Increasing'
        else:
            trend = '→ Stable'
    else:
        absolute_change = None
        trend = 'Insufficient Data'
    
    return {
        'short_history': short_history,
        'absolute_change': round(absolute_change, 2) if absolute_change is not None else None,
        'trend': trend
    }


def collect_all_data(tickers: List[str] = None) -> pd.DataFrame:
    """
    Main function to collect all data for ASX300 stocks
    Returns DataFrame with all metrics for ranking
    """
    if tickers is None:
        tickers = ASX300_TICKERS
    
    print(f"\n{'='*60}")
    print(f"ASX Stock Screener - Data Collection")
    print(f"{'='*60}\n")
    
    # Step 1: Get ASIC short interest data
    short_df = get_asic_short_data(weeks=6)
    
    # Step 2: Get stock data for each ticker
    all_stocks = []
    total = len(tickers)
    
    print(f"\nFetching stock data for {total} tickers...")
    for i, ticker in enumerate(tickers, 1):
        print(f"  [{i}/{total}] {ticker}...", end=' ')
        
        stock_data = get_stock_data(ticker)
        
        if stock_data:
            # Get short interest metrics
            ticker_base = ticker.replace('.AX', '')
            short_metrics = calculate_short_interest_metrics(short_df, ticker_base)
            
            # Combine all data
            stock_data.update({
                'short_history': short_metrics['short_history'],
                'short_absolute_change': short_metrics['absolute_change'],
                'short_trend': short_metrics['trend']
            })
            
            all_stocks.append(stock_data)
            print("✓")
        else:
            print("✗ Failed")
        
        # Small delay to avoid rate limiting
        time.sleep(0.3)
    
    print(f"\nSuccessfully collected data for {len(all_stocks)} stocks")
    
    return pd.DataFrame(all_stocks)


if __name__ == "__main__":
    # Test the data collection
    print("Testing data collection module...\n")
    
    # Test with just a few tickers
    test_tickers = ['BHP.AX', 'CBA.AX', 'CSL.AX']
    df = collect_all_data(test_tickers)
    
    print("\n" + "="*60)
    print("Sample Results:")
    print("="*60)
    print(df[['ticker', 'company_name', 'current_price', 'pe_ratio', 'range_position_pct', 'short_absolute_change']].to_string())
