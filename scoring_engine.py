"""
ASX Stock Screener - Scoring Engine
Calculates composite scores based on:
1. Position in 52-week range (lower is better) - PRIMARY
2. Short interest decline (declining is better) - SECONDARY  
3. P/E ratio (lower is better) - TERTIARY
"""

import pandas as pd
import numpy as np


def normalize_score(value, min_val, max_val, reverse=False):
    """
    Normalize a value to 0-100 scale
    If reverse=True, lower values get higher scores
    """
    if pd.isna(value) or min_val == max_val:
        return 50.0  # Neutral score if no data
    
    normalized = ((value - min_val) / (max_val - min_val)) * 100
    
    if reverse:
        normalized = 100 - normalized
    
    return normalized


def calculate_composite_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate composite score for each stock
    
    Scoring weights:
    - 52-week range position: 50% (lower position = better score)
    - Short interest change: 30% (declining shorts = better score)
    - P/E ratio: 20% (lower P/E = better score)
    """
    
    print("\nCalculating composite scores...")
    
    df_scored = df.copy()
    
    # Filter out stocks with missing critical data
    df_scored = df_scored[df_scored['pe_ratio'].notna()].copy()
    df_scored = df_scored[df_scored['range_position_pct'].notna()].copy()
    
    print(f"  Scoring {len(df_scored)} stocks with complete data")
    
    # 1. Score for 52-week range position (lower is better)
    # Stocks near 52-week lows get high scores
    min_range = df_scored['range_position_pct'].min()
    max_range = df_scored['range_position_pct'].max()
    
    df_scored['range_score'] = df_scored['range_position_pct'].apply(
        lambda x: normalize_score(x, min_range, max_range, reverse=True)
    )
    
    # 2. Score for short interest change (declining is better)
    # Stocks with declining shorts (negative change) get high scores
    # Handle missing short data
    df_scored['short_score'] = 50.0  # Default neutral score
    
    has_short_data = df_scored['short_absolute_change'].notna()
    if has_short_data.sum() > 0:
        short_data = df_scored.loc[has_short_data, 'short_absolute_change']
        min_short = short_data.min()
        max_short = short_data.max()
        
        # Declining shorts (negative change) should get high scores
        df_scored.loc[has_short_data, 'short_score'] = short_data.apply(
            lambda x: normalize_score(x, min_short, max_short, reverse=True)
        )
    
    # 3. Score for P/E ratio (lower is better)
    # Filter out negative P/E ratios (usually means losses)
    valid_pe = (df_scored['pe_ratio'] > 0) & (df_scored['pe_ratio'] < 100)
    
    if valid_pe.sum() > 0:
        pe_data = df_scored.loc[valid_pe, 'pe_ratio']
        min_pe = pe_data.min()
        max_pe = pe_data.max()
        
        df_scored.loc[valid_pe, 'pe_score'] = pe_data.apply(
            lambda x: normalize_score(x, min_pe, max_pe, reverse=True)
        )
    else:
        df_scored['pe_score'] = 50.0
    
    # For invalid P/E (negative or very high), give neutral score
    df_scored.loc[~valid_pe, 'pe_score'] = 50.0
    
    # Calculate weighted composite score
    WEIGHT_RANGE = 0.50      # 50% weight - PRIMARY
    WEIGHT_SHORT = 0.30      # 30% weight - SECONDARY
    WEIGHT_PE = 0.20         # 20% weight - TERTIARY
    
    df_scored['composite_score'] = (
        df_scored['range_score'] * WEIGHT_RANGE +
        df_scored['short_score'] * WEIGHT_SHORT +
        df_scored['pe_score'] * WEIGHT_PE
    )
    
    # Round for display
    df_scored['composite_score'] = df_scored['composite_score'].round(1)
    
    # Sort by composite score (highest first = best opportunities)
    df_scored = df_scored.sort_values('composite_score', ascending=False)
    
    # Add rank
    df_scored['rank'] = range(1, len(df_scored) + 1)
    
    print(f"  ✓ Scoring complete. Top score: {df_scored['composite_score'].max():.1f}")
    
    return df_scored


def format_short_history_display(short_history: list) -> str:
    """
    Format the 6-week short interest history for display
    """
    if not short_history or len(short_history) == 0:
        return "No Data"
    
    # Show last 6 weeks in reverse chronological order (most recent first)
    display_lines = []
    for entry in reversed(short_history[-6:]):  # Last 6 entries, newest first
        date_obj = pd.to_datetime(entry['date'])
        date_str = date_obj.strftime('%d-%b')
        pct = entry['short_pct']
        display_lines.append(f"{date_str}: {pct:.2f}%")
    
    return " | ".join(display_lines)


def prepare_display_dataframe(df_scored: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare final dataframe for display in the UI
    """
    # Select and rename columns for display
    display_df = df_scored[[
        'rank',
        'ticker',
        'company_name',
        'sector',
        'current_price',
        'market_cap',
        'pe_ratio',
        'week52_high',
        'week52_low',
        'range_position_pct',
        'short_history',
        'short_absolute_change',
        'short_trend',
        'composite_score'
    ]].copy()
    
    # Format market cap
    display_df['market_cap_formatted'] = display_df['market_cap'].apply(
        lambda x: f"${x/1e9:.2f}B" if x >= 1e9 else f"${x/1e6:.2f}M" if x >= 1e6 else f"${x:,.0f}"
    )
    
    # Format short history
    display_df['short_history_display'] = display_df['short_history'].apply(
        format_short_history_display
    )
    
    # Rename columns for final display
    display_df = display_df.rename(columns={
        'rank': 'Rank',
        'ticker': 'Ticker',
        'company_name': 'Company',
        'sector': 'Sector',
        'current_price': 'Price ($)',
        'market_cap_formatted': 'Market Cap',
        'pe_ratio': 'P/E',
        'week52_high': '52w High',
        'week52_low': '52w Low',
        'range_position_pct': '52w Position %',
        'short_history_display': 'Short Interest (6 weeks)',
        'short_absolute_change': 'Short Change',
        'short_trend': 'Short Trend',
        'composite_score': 'Score'
    })
    
    # Select final columns
    final_columns = [
        'Rank', 'Ticker', 'Company', 'Sector', 'Price ($)', 'Market Cap',
        'P/E', '52w High', '52w Low', '52w Position %',
        'Short Interest (6 weeks)', 'Short Change', 'Short Trend', 'Score'
    ]
    
    return display_df[final_columns]


if __name__ == "__main__":
    # Test scoring with sample data
    print("Testing scoring engine...")
    
    sample_data = pd.DataFrame([
        {
            'ticker': 'BHP.AX',
            'company_name': 'BHP Group Ltd',
            'sector': 'Materials',
            'current_price': 42.50,
            'market_cap': 215000000000,
            'pe_ratio': 12.5,
            'week52_high': 50.0,
            'week52_low': 38.0,
            'range_position_pct': 37.5,
            'short_history': [{'date': '2025-01-01', 'short_pct': 2.5}],
            'short_absolute_change': -0.5,
            'short_trend': '↓ Declining'
        },
        {
            'ticker': 'CBA.AX',
            'company_name': 'Commonwealth Bank',
            'sector': 'Financials',
            'current_price': 115.0,
            'market_cap': 195000000000,
            'pe_ratio': 18.2,
            'week52_high': 130.0,
            'week52_low': 95.0,
            'range_position_pct': 57.1,
            'short_history': [{'date': '2025-01-01', 'short_pct': 1.2}],
            'short_absolute_change': 0.3,
            'short_trend': '↑ Increasing'
        }
    ])
    
    scored = calculate_composite_score(sample_data)
    display = prepare_display_dataframe(scored)
    
    print("\n" + "="*80)
    print("Sample Scoring Results:")
    print("="*80)
    print(display.to_string(index=False))
