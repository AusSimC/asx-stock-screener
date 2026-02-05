"""
ASX Stock Screener - Main Application
A tool to identify ASX300 stock buying opportunities based on:
- Position in 52-week range
- Short interest trends
- P/E ratio valuation
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys

# Import our custom modules
from data_collector import collect_all_data, ASX300_TICKERS
from scoring_engine import calculate_composite_score, prepare_display_dataframe

# Page configuration
st.set_page_config(
    page_title="ASX Stock Screener",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stDataFrame {
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)


def display_header():
    """Display the main header"""
    st.markdown('<p class="main-header">📈 ASX Stock Screener</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Find undervalued ASX300 stocks with improving sentiment</p>',
        unsafe_allow_html=True
    )


def display_methodology():
    """Display the scoring methodology"""
    with st.expander("ℹ️ How This Works", expanded=False):
        st.markdown("""
        ### Scoring Methodology
        
        This tool ranks ASX300 stocks based on three key factors:
        
        1. **52-Week Range Position (50% weight)** - PRIMARY
           - Stocks trading near their 52-week lows score higher
           - Strategy: Buy when beaten down
           
        2. **Short Interest Trend (30% weight)** - SECONDARY
           - Declining short interest scores higher
           - Strategy: Contrarian signal - shorts are covering
           
        3. **P/E Ratio (20% weight)** - TERTIARY
           - Lower P/E ratios score higher
           - Strategy: Value investing
        
        ### Data Sources
        - **Stock Data**: Yahoo Finance (price, fundamentals, 52-week range)
        - **Short Interest**: ASIC official reports (updated daily with T+4 lag)
        
        ### How to Use
        1. Click "🔄 Run Analysis" to fetch the latest data
        2. Review the ranked list of stocks
        3. Focus on highly-ranked stocks with declining shorts
        4. Conduct your own due diligence before investing
        
        ⚠️ **Disclaimer**: This tool is for informational purposes only. Not financial advice.
        """)


def display_metrics(df: pd.DataFrame):
    """Display summary metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Stocks Analyzed", len(df))
    
    with col2:
        declining_shorts = len(df[df['Short Trend'] == '↓ Declining'])
        st.metric("Stocks with Declining Shorts", declining_shorts)
    
    with col3:
        avg_pe = df['P/E'].mean()
        st.metric("Average P/E Ratio", f"{avg_pe:.1f}")
    
    with col4:
        low_in_range = len(df[df['52w Position %'] < 30])
        st.metric("Stocks < 30% of 52w Range", low_in_range)


def display_filters(df: pd.DataFrame):
    """Display filter options in sidebar"""
    st.sidebar.header("🔍 Filters")
    
    # Sector filter
    all_sectors = ['All'] + sorted(df['Sector'].unique().tolist())
    selected_sector = st.sidebar.selectbox("Sector", all_sectors)
    
    # P/E ratio filter
    pe_max = st.sidebar.slider(
        "Max P/E Ratio",
        min_value=0,
        max_value=50,
        value=30,
        step=1,
        help="Filter out stocks with P/E above this value"
    )
    
    # 52-week position filter
    range_max = st.sidebar.slider(
        "Max 52-Week Position %",
        min_value=0,
        max_value=100,
        value=50,
        step=5,
        help="Only show stocks below this % of their 52-week range"
    )
    
    # Short trend filter
    short_trend_options = st.sidebar.multiselect(
        "Short Interest Trend",
        options=['↓ Declining', '→ Stable', '↑ Increasing', 'No Data', 'Insufficient Data'],
        default=['↓ Declining', '→ Stable'],
        help="Select which short interest trends to include"
    )
    
    return {
        'sector': selected_sector,
        'pe_max': pe_max,
        'range_max': range_max,
        'short_trends': short_trend_options
    }


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Apply filters to the dataframe"""
    filtered = df.copy()
    
    # Sector filter
    if filters['sector'] != 'All':
        filtered = filtered[filtered['Sector'] == filters['sector']]
    
    # P/E filter
    filtered = filtered[
        (filtered['P/E'].isna()) | (filtered['P/E'] <= filters['pe_max'])
    ]
    
    # 52-week position filter
    filtered = filtered[filtered['52w Position %'] <= filters['range_max']]
    
    # Short trend filter
    if filters['short_trends']:
        filtered = filtered[filtered['Short Trend'].isin(filters['short_trends'])]
    
    # Re-rank after filtering
    filtered = filtered.copy()
    filtered['Rank'] = range(1, len(filtered) + 1)
    
    return filtered


def main():
    """Main application logic"""
    
    # Display header
    display_header()
    display_methodology()
    
    # Sidebar
    st.sidebar.title("⚙️ Settings")
    
    # Run analysis button
    if st.sidebar.button("🔄 Run Analysis", type="primary", use_container_width=True):
        with st.spinner("🔄 Fetching data... This may take a few minutes..."):
            try:
                # Collect data
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("Fetching ASIC short interest data...")
                progress_bar.progress(20)
                
                status_text.text("Fetching stock data from Yahoo Finance...")
                progress_bar.progress(40)
                
                # Collect all data
                df_raw = collect_all_data(ASX300_TICKERS)
                
                status_text.text("Calculating scores...")
                progress_bar.progress(70)
                
                # Calculate scores
                df_scored = calculate_composite_score(df_raw)
                
                status_text.text("Preparing results...")
                progress_bar.progress(90)
                
                # Prepare for display
                df_display = prepare_display_dataframe(df_scored)
                
                # Store in session state
                st.session_state['data'] = df_display
                st.session_state['last_updated'] = datetime.now()
                
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                
                st.success(f"Successfully analyzed {len(df_display)} stocks!")
                
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                st.exception(e)
                return
    
    # Display results if available
    if 'data' in st.session_state:
        df = st.session_state['data']
        last_updated = st.session_state['last_updated']
        
        st.sidebar.markdown("---")
        st.sidebar.info(f"**Last Updated:**\n{last_updated.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Display filters
        filters = display_filters(df)
        
        # Apply filters
        df_filtered = apply_filters(df, filters)
        
        st.markdown("---")
        
        # Display metrics
        display_metrics(df_filtered)
        
        st.markdown("---")
        
        # Display results
        st.subheader(f"📊 Results ({len(df_filtered)} stocks)")
        
        # Download button
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name=f"asx_screener_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        # Display the dataframe
        st.dataframe(
            df_filtered,
            use_container_width=True,
            height=600,
            hide_index=True
        )
        
        # Top 10 stocks
        st.markdown("---")
        st.subheader("🏆 Top 10 Opportunities")
        
        top_10 = df_filtered.head(10)
        
        for idx, row in top_10.iterrows():
            with st.expander(f"#{row['Rank']} - {row['Ticker']} - {row['Company']} (Score: {row['Score']})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**📊 Price & Valuation**")
                    st.write(f"Current Price: ${row['Price ($)']:.2f}")
                    st.write(f"P/E Ratio: {row['P/E']:.1f}" if pd.notna(row['P/E']) else "P/E Ratio: N/A")
                    st.write(f"Market Cap: {row['Market Cap']}")
                
                with col2:
                    st.markdown("**📈 52-Week Range**")
                    st.write(f"52w High: ${row['52w High']:.2f}")
                    st.write(f"52w Low: ${row['52w Low']:.2f}")
                    st.write(f"Position: {row['52w Position %']:.1f}%")
                
                with col3:
                    st.markdown("**📉 Short Interest**")
                    st.write(f"Trend: {row['Short Trend']}")
                    if pd.notna(row['Short Change']):
                        st.write(f"6-Week Change: {row['Short Change']:.2f}%")
                    st.write(f"Sector: {row['Sector']}")
    
    else:
        # No data yet - show instructions
        st.info("👈 Click '🔄 Run Analysis' in the sidebar to get started!")
        
        st.markdown("---")
        st.markdown("""
        ### What You'll Get:
        - ✅ All ASX300 stocks ranked by opportunity score
        - ✅ 6-week short interest trends
        - ✅ Current position in 52-week price range
        - ✅ P/E ratios and market caps
        - ✅ Sector information for diversification
        - ✅ Downloadable results in CSV format
        
        ### Data Freshness:
        - Stock prices: Real-time from Yahoo Finance
        - Short interest: ASIC official reports (T+4 lag)
        - Analysis runs on-demand when you click the button
        """)


if __name__ == "__main__":
    main()
