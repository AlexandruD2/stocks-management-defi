"""
Streamlit Dashboard for Stocks Portfolio Management
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from database_manager import DatabaseManager
from data_collection import DataCollector
from analysis import StockAnalyzer
from config import TICKERS, ALL_TICKERS, TICKER_NAMES

# Page configuration
st.set_page_config(
    page_title="Stocks Management Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
db = DatabaseManager()

# User-friendly signal reason mapping
SIGNAL_REASONS = {
    "price_below_sma20": "Price below 20-day moving average - Downtrend signal",
    "price_above_sma20": "Price above 20-day moving average - Uptrend signal",
    "moving_average_golden_cross": "Golden Cross! (SMA20 > SMA50 > SMA200) - Strong BUY setup",
    "moving_average_death_cross": "Death Cross (SMA20 < SMA50 < SMA200) - Strong SELL setup",
    "dividend_yield_increase": "Dividend yield increasing - Income opportunity",
    "dividend_yield_decrease": "Dividend yield decreasing - Warning signal",
    "consistent_positive_earnings": "Consistent positive earnings surprises - Quality company",
    "negative_earnings_surprise": "Recent negative earnings surprises - Caution",
    "low_pe_valuation": "Low PE ratio - Undervalued, potential value buy",
    "high_pe_valuation": "High PE ratio - Overvalued, potential sell"
}

def get_friendly_reason(reason):
    """Convert technical reason to user-friendly description"""
    return SIGNAL_REASONS.get(reason, reason)

st.title("📊 Stock Portfolio Management Dashboard")
st.markdown("Real-time monitoring of multi-sector stock portfolio with AI-driven buy/sell signals")

# Sidebar for controls
with st.sidebar:
    st.header("⚙️ Controls")

    if st.button("🔄 Refresh Data", help="Update data and regenerate signals"):
        with st.spinner("Updating data..."):
            collector = DataCollector()
            collector.update_daily_data()

            analyzer = StockAnalyzer()
            analyzer.analyze_all_stocks()

        st.success("Data updated successfully!")

    if st.button("🚀 Full Pipeline Run", help="Complete data collection and analysis"):
        with st.spinner("Running full pipeline..."):
            collector = DataCollector()
            collector.collect_all_data()

            analyzer = StockAnalyzer()
            analyzer.analyze_all_stocks()

        st.success("Pipeline completed!")

    st.divider()

    # Sector selector
    sectors = list(TICKERS.keys())
    selected_sector = st.selectbox("Filter by Sector", ["All Sectors"] + sectors)

    if selected_sector == "All Sectors":
        filtered_tickers = ALL_TICKERS
    else:
        filtered_tickers = TICKERS[selected_sector]

    st.divider()
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# Main dashboard layout
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📈 Signals",
    "💼 Portfolio",
    "📊 Performance",
    "🔍 Fundamentals",
    "📅 Historical",
    "📉 Volatility",
    "💎 Defi",
    "🎯 Swing Trading",
    "📊 Daily Price Log"
])

# TAB 1: BUY/SELL SIGNALS
with tab1:
    st.subheader("Recent Buy/Sell Signals")

    signals = db.get_latest_signals(days=30)
    signals_df = pd.DataFrame(
        signals,
        columns=["Ticker", "Signal Type", "Reason", "Strength", "Date"]
    )

    if not signals_df.empty:
        # Convert reasons to user-friendly format
        signals_df["Reason"] = signals_df["Reason"].apply(get_friendly_reason)

        # Filter by selected sector
        signals_df = signals_df[signals_df["Ticker"].isin(filtered_tickers)]

        col1, col2, col3 = st.columns(3)

        with col1:
            buy_count = len(signals_df[signals_df["Signal Type"] == "BUY"])
            st.metric("🟢 BUY Signals", buy_count)

        with col2:
            sell_count = len(signals_df[signals_df["Signal Type"] == "SELL"])
            st.metric("🔴 SELL Signals", sell_count)

        with col3:
            avg_strength = signals_df["Strength"].mean()
            st.metric("📊 Avg Signal Strength", f"{avg_strength:.1f}")

        st.divider()

        # Display signals by type
        col1, col2 = st.columns(2)

        with col1:
            buy_signals = signals_df[signals_df["Signal Type"] == "BUY"].head(10)
            if not buy_signals.empty:
                st.subheader("🟢 Buy Signals")
                display_buy = buy_signals[["Ticker", "Reason", "Strength", "Date"]].copy()
                display_buy["Strength"] = display_buy["Strength"].apply(lambda x: f"{x:.0f}/100")
                st.dataframe(
                    display_buy,
                    use_container_width=True,
                    hide_index=True
                )

        with col2:
            sell_signals = signals_df[signals_df["Signal Type"] == "SELL"].head(10)
            if not sell_signals.empty:
                st.subheader("🔴 Sell Signals")
                display_sell = sell_signals[["Ticker", "Reason", "Strength", "Date"]].copy()
                display_sell["Strength"] = display_sell["Strength"].apply(lambda x: f"{x:.0f}/100")
                st.dataframe(
                    display_sell,
                    use_container_width=True,
                    hide_index=True
                )

        # Signal strength distribution
        st.subheader("Signal Strength Distribution")
        fig = px.histogram(
            signals_df,
            x="Strength",
            color="Signal Type",
            nbins=20,
            color_discrete_map={"BUY": "#2ecc71", "SELL": "#e74c3c"}
        )
        fig.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No signals available yet. Run the pipeline first!")


# TAB 2: PORTFOLIO
with tab2:
    st.subheader("Portfolio Holdings")

    portfolio = db.get_portfolio()
    portfolio_df = pd.DataFrame(
        portfolio,
        columns=["Ticker", "Shares Owned", "Average Cost", "Date Added"]
    )

    if not portfolio_df.empty:
        portfolio_df = portfolio_df[portfolio_df["Ticker"].isin(filtered_tickers)]

        if not portfolio_df.empty:
            # Add current prices
            current_prices = []
            for ticker in portfolio_df["Ticker"]:
                fundamentals = db.get_latest_fundamentals(ticker)
                if fundamentals:
                    current_prices.append(fundamentals[2])  # price is index 2
                else:
                    current_prices.append(None)

            portfolio_df["Current Price"] = current_prices
            portfolio_df["Current Value"] = portfolio_df["Shares Owned"] * portfolio_df["Current Price"]
            portfolio_df["Gain/Loss"] = portfolio_df["Current Value"] - (portfolio_df["Shares Owned"] * portfolio_df["Average Cost"])
            portfolio_df["Gain/Loss %"] = (portfolio_df["Gain/Loss"] / (portfolio_df["Shares Owned"] * portfolio_df["Average Cost"]) * 100).round(2)

            col1, col2, col3 = st.columns(3)

            with col1:
                total_value = portfolio_df["Current Value"].sum()
                st.metric("💰 Total Portfolio Value", f"${total_value:,.2f}")

            with col2:
                total_gain = portfolio_df["Gain/Loss"].sum()
                st.metric("📈 Total Gain/Loss", f"${total_gain:,.2f}")

            with col3:
                total_return = (total_gain / (portfolio_df["Shares Owned"] * portfolio_df["Average Cost"]).sum() * 100) if (portfolio_df["Shares Owned"] * portfolio_df["Average Cost"]).sum() > 0 else 0
                st.metric("📊 Total Return %", f"{total_return:.2f}%")

            st.divider()

            st.dataframe(
                portfolio_df[["Ticker", "Shares Owned", "Average Cost", "Current Price", "Current Value", "Gain/Loss", "Gain/Loss %"]],
                use_container_width=True,
                hide_index=True
            )

            # Portfolio allocation pie chart
            st.subheader("Portfolio Allocation")
            fig = px.pie(
                portfolio_df,
                values="Current Value",
                names="Ticker",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No holdings in selected sector.")
    else:
        st.info("Portfolio is empty. Add holdings to track performance!")


# TAB 3: PERFORMANCE METRICS
with tab3:
    st.subheader("Performance Analysis")

    # Get all fundamentals for filtered tickers
    performance_data = []
    for ticker in filtered_tickers:
        fund = db.get_latest_fundamentals(ticker)
        if fund:
            # fund structure: id(0), ticker(1), date(2), price(3), pe_ratio(4), dividend_yield(5), market_cap(6), revenue(7), net_income(8), book_value(9), eps(10)
            performance_data.append({
                "Ticker": ticker,
                "Price": fund[3],
                "PE Ratio": fund[4],
                "Dividend Yield %": fund[5],
                "EPS": fund[10]
            })

    if performance_data:
        perf_df = pd.DataFrame(performance_data)

        # Convert to numeric types
        perf_df["Price"] = pd.to_numeric(perf_df["Price"], errors="coerce")
        perf_df["PE Ratio"] = pd.to_numeric(perf_df["PE Ratio"], errors="coerce")
        perf_df["Dividend Yield %"] = pd.to_numeric(perf_df["Dividend Yield %"], errors="coerce")
        perf_df["EPS"] = pd.to_numeric(perf_df["EPS"], errors="coerce")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            avg_pe = perf_df["PE Ratio"].mean()
            st.metric("📊 Avg PE Ratio", f"{avg_pe:.2f}" if not pd.isna(avg_pe) else "N/A")

        with col2:
            avg_div = perf_df["Dividend Yield %"].mean()
            st.metric("💵 Avg Dividend Yield", f"{avg_div:.2f}%" if not pd.isna(avg_div) else "N/A")

        with col3:
            high_price = perf_df["Price"].max()
            st.metric("📈 Highest Price", f"${high_price:.2f}" if not pd.isna(high_price) else "N/A")

        with col4:
            low_price = perf_df["Price"].min()
            st.metric("📉 Lowest Price", f"${low_price:.2f}" if not pd.isna(low_price) else "N/A")

        st.divider()

        # PE Ratio comparison
        col1, col2 = st.columns(2)

        with col1:
            fig = px.scatter(
                perf_df,
                x="PE Ratio",
                y="Dividend Yield %",
                hover_data=["Ticker", "Price"],
                labels={"PE Ratio": "P/E Ratio", "Dividend Yield %": "Dividend Yield (%)"},
                height=400
            )
            fig.update_traces(marker=dict(size=10, color="#3498db"))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.bar(
                perf_df.sort_values("PE Ratio"),
                x="Ticker",
                y="PE Ratio",
                color="PE Ratio",
                color_continuous_scale="RdYlGn_r",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

        st.dataframe(perf_df, use_container_width=True, hide_index=True)
    else:
        st.info("No performance data available yet.")


# TAB 4: FUNDAMENTALS
with tab4:
    st.subheader("Stock Fundamentals")

    selected_ticker = st.selectbox(
        "Select Stock", filtered_tickers,
        format_func=lambda t: f"{TICKER_NAMES.get(t, t)} ({t})"
    )

    if selected_ticker:
        fund = db.get_latest_fundamentals(selected_ticker)

        if fund:
            # Convert to float for safe formatting
            # fund structure: id(0), ticker(1), date(2), price(3), pe_ratio(4), dividend_yield(5), market_cap(6), revenue(7), net_income(8), book_value(9), eps(10)
            price = float(fund[3]) if fund[3] else None
            pe = float(fund[4]) if fund[4] else None
            div = float(fund[5]) if fund[5] else None
            mcap = float(fund[6]) if fund[6] else None
            revenue = float(fund[7]) if fund[7] else None
            net_income = float(fund[8]) if fund[8] else None
            book_val = float(fund[9]) if fund[9] else None
            eps = float(fund[10]) if fund[10] else None

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Price", f"${price:.2f}" if price else "N/A")

            with col2:
                st.metric("PE Ratio", f"{pe:.2f}" if pe else "N/A")

            with col3:
                st.metric("Dividend Yield", f"{div:.2f}%" if div else "N/A")

            with col4:
                st.metric("EPS", f"${eps:.2f}" if eps else "N/A")

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Market Cap", f"${mcap/1e9:.2f}B" if mcap else "N/A")
                st.metric("Revenue", f"${revenue/1e9:.2f}B" if revenue else "N/A")

            with col2:
                st.metric("Net Income", f"${net_income/1e9:.2f}B" if net_income else "N/A")
                st.metric("Book Value", f"${book_val:.2f}" if book_val else "N/A")

            st.divider()

            # Price history
            st.subheader(f"{selected_ticker} - Price History (Last 90 Days)")
            prices = db.get_daily_prices(selected_ticker, days=90)

            if prices:
                prices_df = pd.DataFrame(
                    prices,
                    columns=["Date", "Open", "Close", "High", "Low", "Volume"]
                )
                prices_df = prices_df.sort_values("Date")

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=prices_df["Date"],
                    y=prices_df["Close"],
                    mode="lines",
                    name="Close Price",
                    line=dict(color="#3498db", width=2)
                ))
                fig.add_trace(go.Scatter(
                    x=prices_df["Date"],
                    y=prices_df["High"],
                    mode="lines",
                    name="High",
                    line=dict(color="#2ecc71", width=1, dash="dot")
                ))
                fig.add_trace(go.Scatter(
                    x=prices_df["Date"],
                    y=prices_df["Low"],
                    mode="lines",
                    name="Low",
                    line=dict(color="#e74c3c", width=1, dash="dot")
                ))

                fig.update_layout(height=400, hovermode="x unified")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"No fundamental data available for {selected_ticker}")


# TAB 5: HISTORICAL DATA
with tab5:
    st.subheader("Historical Price Data")

    selected_ticker = st.selectbox(
        "Select Stock for Historical Analysis", filtered_tickers, key="history_ticker",
        format_func=lambda t: f"{TICKER_NAMES.get(t, t)} ({t})"
    )
    days_lookback = st.slider("Days to Display", 30, 365, 90)

    if selected_ticker:
        # Get company name
        company_name = TICKER_NAMES.get(selected_ticker, selected_ticker)
        stock_display = f"{company_name} - {selected_ticker}"

        prices = db.get_daily_prices(selected_ticker, days=days_lookback)

        if prices:
            prices_df = pd.DataFrame(
                prices,
                columns=["Date", "Open", "Close", "High", "Low", "Volume"]
            )
            prices_df = prices_df.sort_values("Date")
            prices_df["Open-Close Diff"] = prices_df["Close"] - prices_df["Open"]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Avg Close Price", f"${prices_df['Close'].mean():.2f}")

            with col2:
                st.metric("Max Price", f"${prices_df['High'].max():.2f}")

            with col3:
                st.metric("Min Price", f"${prices_df['Low'].min():.2f}")

            st.divider()

            # Candlestick chart
            fig = go.Figure(data=[go.Candlestick(
                x=prices_df["Date"],
                open=prices_df["Open"],
                high=prices_df["High"],
                low=prices_df["Low"],
                close=prices_df["Close"]
            )])

            fig.update_layout(
                title=f"{stock_display} - Historical Price Data",
                height=500,
                xaxis_rangeslider_visible=False
            )
            st.plotly_chart(fig, use_container_width=True)

            # Volume analysis
            fig = px.bar(prices_df, x="Date", y="Volume", title=f"{stock_display} - Trading Volume")
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

            # Display data table
            st.subheader(f"Data Table - {stock_display}")
            st.dataframe(prices_df, use_container_width=True, hide_index=True)
        else:
            st.info(f"No historical data available for {stock_display}")


# TAB 6: VOLATILITY & PRICE ACTION
with tab6:
    st.subheader("Volatility & Price Action Analysis")

    # Quick preset selections
    st.markdown("### Quick Comparisons")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("Tech", key="btn_tech"):
            st.session_state.selected_stocks = ["AAPL", "MSFT", "NVDA"]

    with col2:
        if st.button("Energy", key="btn_energy"):
            st.session_state.selected_stocks = ["XOM", "CVX", "COP"]

    with col3:
        if st.button("Healthcare", key="btn_health"):
            st.session_state.selected_stocks = ["JNJ", "UNH", "PFE"]

    with col4:
        if st.button("AI Leaders", key="btn_ai"):
            st.session_state.selected_stocks = ["NVDA", "TSLA", "PLTR"]

    with col5:
        if st.button("Top Performers", key="btn_top"):
            st.session_state.selected_stocks = ["CAT", "GOOGL", "MPC"]

    st.divider()

    # Manual stock selection
    st.markdown("### Select Stocks Manually")
    selected_stocks = st.multiselect(
        "Choose stocks to analyze:",
        ALL_TICKERS,
        default=st.session_state.get("selected_stocks", ["NVDA", "AAPL", "JNJ"]),
        key="stock_selector"
    )

    # Timeframe selection
    col1, col2, col3 = st.columns(3)
    with col1:
        days_range = st.slider("Days of History", 10, 252, 60, help="Higher = More data for momentum analysis", key="days_slider_unique")
    with col2:
        st.write("")
    with col3:
        st.write("")

    if selected_stocks:
        st.divider()

        # Create combined analysis for all selected stocks
        all_volatility_data = []
        data_loaded = []

        for ticker in selected_stocks:
            prices = db.get_daily_prices(ticker, days=days_range)

            if prices:
                data_loaded.append(f"{ticker} ({len(prices)} days)")
            else:
                data_loaded.append(f"{ticker} (no data)")

            if prices:
                prices_df = pd.DataFrame(
                    prices,
                    columns=["Date", "Open", "Close", "High", "Low", "Volume"]
                )
                prices_df = prices_df.sort_values("Date")

                # Calculate volatility metrics
                prices_df["Daily_Range"] = prices_df["High"] - prices_df["Low"]
                prices_df["Daily_Change"] = prices_df["Close"] - prices_df["Open"]
                prices_df["Daily_Change_Pct"] = (prices_df["Daily_Change"] / prices_df["Open"] * 100).round(2)
                prices_df["Volatility_Pct"] = (prices_df["Daily_Range"] / prices_df["Open"] * 100).round(2)

                # Add ticker column
                prices_df["Ticker"] = ticker

                all_volatility_data.append(prices_df)

        # Show data loading status
        if data_loaded:
            st.info(f"📊 Data loaded: {', '.join(data_loaded)}")

        if all_volatility_data:
            combined_df = pd.concat(all_volatility_data, ignore_index=True)

            # Summary metrics by stock
            st.markdown("### Volatility Summary")

            summary_stats = []
            for ticker in selected_stocks:
                ticker_data = combined_df[combined_df["Ticker"] == ticker]
                if not ticker_data.empty:
                    avg_vol = ticker_data["Volatility_Pct"].mean()
                    max_vol = ticker_data["Volatility_Pct"].max()
                    avg_change = ticker_data["Daily_Change_Pct"].mean()
                    win_rate = (len(ticker_data[ticker_data["Daily_Change_Pct"] > 0]) / len(ticker_data) * 100)
                    current_price = ticker_data["Close"].iloc[-1]

                    summary_stats.append({
                        "Ticker": ticker,
                        "Price": f"${current_price:.2f}",
                        "Avg Vol %": f"{avg_vol:.2f}%",
                        "Max Vol %": f"{max_vol:.2f}%",
                        "Avg Change %": f"{avg_change:+.2f}%",
                        "Win Rate": f"{win_rate:.0f}%"
                    })

            if summary_stats:
                summary_df = pd.DataFrame(summary_stats)
                st.dataframe(summary_df, use_container_width=True, hide_index=True)

            st.divider()

            # Volatility chart - simple line
            st.markdown("### Volatility Trend")
            fig = px.line(
                combined_df,
                x="Date",
                y="Volatility_Pct",
                color="Ticker",
                markers=True,
                height=350
            )
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig, use_container_width=True)

            # Daily change chart
            st.markdown("### Daily Price Change")
            fig = px.bar(
                combined_df,
                x="Date",
                y="Daily_Change_Pct",
                color="Ticker",
                barmode="group",
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)

            # Expandable detailed tables by stock
            st.divider()
            st.markdown("### Detailed OHLC Data & Momentum")

            with st.expander("Show complete price history with momentum analysis"):
                for ticker in selected_stocks:
                    ticker_data = combined_df[combined_df["Ticker"] == ticker].copy()

                    if not ticker_data.empty:
                        # Sort by date ascending for momentum calculations
                        ticker_data = ticker_data.sort_values("Date")

                        # Calculate momentum indicators
                        ticker_data["5D_Avg"] = ticker_data["Close"].rolling(window=5, min_periods=1).mean()
                        ticker_data["Momentum"] = ticker_data["Close"] - ticker_data["5D_Avg"]
                        ticker_data["Trend"] = ticker_data["Momentum"].apply(
                            lambda x: "UP" if x > 0.5 else "DOWN" if x < -0.5 else "NEUTRAL"
                        )

                        # Create display dataframe
                        display_df = ticker_data[[
                            "Date", "Open", "High", "Low", "Close",
                            "Daily_Change_Pct", "Volatility_Pct", "5D_Avg", "Momentum", "Trend", "Volume"
                        ]].copy()

                        display_df = display_df.rename(columns={
                            "Daily_Change_Pct": "Chg %",
                            "Volatility_Pct": "Vol %",
                            "5D_Avg": "5D Avg",
                            "Momentum": "Mom",
                            "Trend": "Trend",
                            "Volume": "Vol"
                        })

                        # Format for display
                        display_df["Open"] = display_df["Open"].apply(lambda x: f"${x:.2f}")
                        display_df["High"] = display_df["High"].apply(lambda x: f"${x:.2f}")
                        display_df["Low"] = display_df["Low"].apply(lambda x: f"${x:.2f}")
                        display_df["Close"] = display_df["Close"].apply(lambda x: f"${x:.2f}")
                        display_df["Chg %"] = display_df["Chg %"].apply(lambda x: f"{x:+.2f}%")
                        display_df["Vol %"] = display_df["Vol %"].apply(lambda x: f"{x:.2f}%")
                        display_df["5D Avg"] = display_df["5D Avg"].apply(lambda x: f"${x:.2f}")
                        display_df["Mom"] = display_df["Mom"].apply(lambda x: f"{x:+.2f}")
                        display_df["Vol"] = display_df["Vol"].apply(lambda x: f"{int(x/1e6):.1f}M" if x > 1e6 else f"{int(x/1e3):.0f}K")

                        # Display header with stats
                        col1, col2, col3, col4, col5 = st.columns(5)
                        with col1:
                            st.metric(f"{ticker} Current", f"${ticker_data['Close'].iloc[-1]:.2f}")
                        with col2:
                            period_change = ((ticker_data['Close'].iloc[-1] - ticker_data['Close'].iloc[0]) / ticker_data['Close'].iloc[0] * 100)
                            st.metric("Period Change", f"{period_change:+.2f}%")
                        with col3:
                            latest_trend = display_df["Trend"].iloc[-1]
                            st.metric("Current Trend", latest_trend)
                        with col4:
                            avg_vol = ticker_data["Volatility_Pct"].mean()
                            st.metric("Avg Volatility", f"{avg_vol:.2f}%")
                        with col5:
                            records = len(ticker_data)
                            st.metric("Trading Days", records)

                        st.write("")

                        # Display the full table
                        st.dataframe(
                            display_df.sort_values("Date", ascending=False),
                            use_container_width=True,
                            hide_index=True,
                            height=600  # Show more rows at once
                        )

                        # Add analysis notes
                        latest_momentum = ticker_data["Momentum"].iloc[-1]
                        recent_avg = ticker_data["Momentum"].tail(5).mean()

                        st.markdown(f"""
                        **Momentum Analysis:**
                        - Latest momentum: {latest_momentum:+.2f} (vs 5D avg: {ticker_data["5D_Avg"].iloc[-1]:.2f})
                        - Recent 5-day trend: {'BULLISH' if recent_avg > 0 else 'BEARISH'}
                        - Higher volatility = More trading opportunity | Lower volatility = More stable
                        """)

                        st.divider()
    else:
        st.info("👆 Click a preset or select stocks above to get started!")


# TAB 7: DEFI - OPEN/CLOSE PERFORMANCE ANALYSIS
with tab7:
    st.subheader("Defi Performance Analysis")
    st.markdown("Automatic ranking of stocks by Open-Close price movements")

    # Timeframe selector
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        days_range = st.slider("Analysis Period (days)", 1, 60, 7, key="defi_days")
    with col2:
        st.write("")
        st.write("")
        if st.button("🔄 Refresh Analysis"):
            st.rerun()
    with col3:
        st.write("")

    st.divider()

    # Analyze all stocks
    analysis_data = []

    for ticker in filtered_tickers:
        try:
            prices = db.get_daily_prices(ticker, days=days_range)
            if prices and len(prices) > 0:
                prices_df = pd.DataFrame(
                    prices,
                    columns=["Date", "Open", "Close", "High", "Low", "Volume"]
                )
                prices_df = prices_df.sort_values("Date")
                prices_df["Diff"] = prices_df["Close"] - prices_df["Open"]
                prices_df["Diff_Pct"] = (prices_df["Diff"] / prices_df["Open"] * 100)

                # Calculate metrics
                total_diff = prices_df["Diff"].sum()
                avg_diff = prices_df["Diff"].mean()
                max_diff = prices_df["Diff"].max()
                min_diff = prices_df["Diff"].min()
                winning_days = len(prices_df[prices_df["Diff"] > 0])
                losing_days = len(prices_df[prices_df["Diff"] < 0])
                total_days = len(prices_df)
                win_rate = (winning_days / total_days * 100) if total_days > 0 else 0

                latest_price = prices_df["Close"].iloc[-1]
                latest_diff = prices_df["Diff"].iloc[-1]

                analysis_data.append({
                    "Ticker": ticker,
                    "Latest Price": latest_price,
                    "Today Diff": latest_diff,
                    "Total Diff": total_diff,
                    "Avg Diff": avg_diff,
                    "Max Move": max_diff,
                    "Min Move": min_diff,
                    "Win Rate %": win_rate,
                    "Winning Days": winning_days,
                    "Losing Days": losing_days,
                    "Days": total_days
                })
        except Exception as e:
            continue

    if analysis_data:
        analysis_df = pd.DataFrame(analysis_data)

        # Display tabs for different rankings
        rank_tab1, rank_tab2, rank_tab3, rank_tab4 = st.tabs([
            "🚀 Best Overall Performers",
            "📈 Best Today",
            "🔴 Biggest Losers",
            "💰 Highest Win Rate"
        ])

        with rank_tab1:
            st.markdown("### Ranked by Total Cumulative Difference")
            top_performers = analysis_df.nlargest(15, "Total Diff")[
                ["Ticker", "Latest Price", "Total Diff", "Avg Diff", "Win Rate %", "Days"]
            ].copy()
            top_performers["Total Diff"] = top_performers["Total Diff"].apply(lambda x: f"${x:+.2f}")
            top_performers["Avg Diff"] = top_performers["Avg Diff"].apply(lambda x: f"${x:+.2f}")
            top_performers["Latest Price"] = top_performers["Latest Price"].apply(lambda x: f"${x:.2f}")
            top_performers["Win Rate %"] = top_performers["Win Rate %"].apply(lambda x: f"{x:.1f}%")
            st.dataframe(top_performers, use_container_width=True, hide_index=True)

            # Chart
            chart_data = analysis_df.nlargest(10, "Total Diff")
            fig = px.bar(
                chart_data,
                x="Ticker",
                y="Total Diff",
                title="Top 10 Cumulative Gainers",
                color="Total Diff",
                color_continuous_scale="RdYlGn"
            )
            st.plotly_chart(fig, use_container_width=True)

        with rank_tab2:
            st.markdown("### Ranked by Today's Move (Latest Day)")
            today_best = analysis_df.nlargest(15, "Today Diff")[
                ["Ticker", "Latest Price", "Today Diff", "Avg Diff", "Win Rate %", "Days"]
            ].copy()
            today_best["Today Diff"] = today_best["Today Diff"].apply(lambda x: f"${x:+.2f}")
            today_best["Avg Diff"] = today_best["Avg Diff"].apply(lambda x: f"${x:+.2f}")
            today_best["Latest Price"] = today_best["Latest Price"].apply(lambda x: f"${x:.2f}")
            today_best["Win Rate %"] = today_best["Win Rate %"].apply(lambda x: f"{x:.1f}%")
            st.dataframe(today_best, use_container_width=True, hide_index=True)

            # Chart
            chart_data = analysis_df.nlargest(10, "Today Diff")
            fig = px.bar(
                chart_data,
                x="Ticker",
                y="Today Diff",
                title="Top 10 Today's Gainers",
                color="Today Diff",
                color_continuous_scale="RdYlGn"
            )
            st.plotly_chart(fig, use_container_width=True)

        with rank_tab3:
            st.markdown("### Ranked by Biggest Losses")
            worst_performers = analysis_df.nsmallest(15, "Total Diff")[
                ["Ticker", "Latest Price", "Total Diff", "Avg Diff", "Win Rate %", "Days"]
            ].copy()
            worst_performers["Total Diff"] = worst_performers["Total Diff"].apply(lambda x: f"${x:+.2f}")
            worst_performers["Avg Diff"] = worst_performers["Avg Diff"].apply(lambda x: f"${x:+.2f}")
            worst_performers["Latest Price"] = worst_performers["Latest Price"].apply(lambda x: f"${x:.2f}")
            worst_performers["Win Rate %"] = worst_performers["Win Rate %"].apply(lambda x: f"{x:.1f}%")
            st.dataframe(worst_performers, use_container_width=True, hide_index=True)

            # Chart
            chart_data = analysis_df.nsmallest(10, "Total Diff")
            fig = px.bar(
                chart_data,
                x="Ticker",
                y="Total Diff",
                title="Top 10 Biggest Losers",
                color="Total Diff",
                color_continuous_scale="RdYlGn"
            )
            st.plotly_chart(fig, use_container_width=True)

        with rank_tab4:
            st.markdown("### Ranked by Win Rate (% of Profitable Days)")
            best_winrate = analysis_df.nlargest(15, "Win Rate %")[
                ["Ticker", "Latest Price", "Win Rate %", "Winning Days", "Losing Days", "Total Diff"]
            ].copy()
            best_winrate["Latest Price"] = best_winrate["Latest Price"].apply(lambda x: f"${x:.2f}")
            best_winrate["Win Rate %"] = best_winrate["Win Rate %"].apply(lambda x: f"{x:.1f}%")
            best_winrate["Total Diff"] = best_winrate["Total Diff"].apply(lambda x: f"${x:+.2f}")
            st.dataframe(best_winrate, use_container_width=True, hide_index=True)

            # Chart
            chart_data = analysis_df.nlargest(10, "Win Rate %")
            fig = px.bar(
                chart_data,
                x="Ticker",
                y="Win Rate %",
                title="Top 10 Consistent Winners (By Win Rate)",
                color="Win Rate %",
                color_continuous_scale="Greens"
            )
            fig.update_yaxes(range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)

        # Summary statistics
        st.divider()
        st.subheader("Portfolio Summary")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Total Stocks Analyzed", len(analysis_df))
        with col2:
            avg_total_diff = analysis_df["Total Diff"].mean()
            st.metric("Avg Cumulative Diff", f"${avg_total_diff:+.2f}")
        with col3:
            avg_winrate = analysis_df["Win Rate %"].mean()
            st.metric("Avg Win Rate", f"{avg_winrate:.1f}%")
        with col4:
            best_ticker = analysis_df.loc[analysis_df["Total Diff"].idxmax(), "Ticker"]
            best_value = analysis_df["Total Diff"].max()
            st.metric("Top Performer", f"{best_ticker}: ${best_value:+.2f}")
        with col5:
            worst_ticker = analysis_df.loc[analysis_df["Total Diff"].idxmin(), "Ticker"]
            worst_value = analysis_df["Total Diff"].min()
            st.metric("Worst Performer", f"{worst_ticker}: ${worst_value:+.2f}")

    else:
        st.warning("No data available for analysis. Please run backfill_history.py first.")


# TAB 8: SWING TRADING - SHORT-TERM PROFIT SIGNALS
with tab8:
    st.subheader("Swing Trading Analysis")
    st.markdown("Identify stocks with consistent daily volatility for 1-2 day holding periods")

    # Analysis parameters
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        swing_days = st.slider("Analysis Period (days)", 5, 60, 20, key="swing_days")
    with col2:
        min_volume_filter = st.number_input("Min Avg Volume (M)", 1, 100, 5, key="min_vol")
    with col3:
        st.write("")

    st.divider()

    # Analyze all stocks for swing trading potential
    swing_data = []

    for ticker in filtered_tickers:
        try:
            prices = db.get_daily_prices(ticker, days=swing_days)
            if prices and len(prices) > 5:
                prices_df = pd.DataFrame(
                    prices,
                    columns=["Date", "Open", "Close", "High", "Low", "Volume"]
                )
                prices_df = prices_df.sort_values("Date")
                prices_df["Daily_Swing"] = abs(prices_df["Close"] - prices_df["Open"])
                prices_df["Swing_Pct"] = (prices_df["Daily_Swing"] / prices_df["Open"] * 100)
                prices_df["Direction"] = (prices_df["Close"] - prices_df["Open"]) / abs(prices_df["Close"] - prices_df["Open"])

                # Calculate swing trading metrics
                avg_swing = prices_df["Daily_Swing"].mean()
                avg_swing_pct = prices_df["Swing_Pct"].mean()
                max_swing = prices_df["Daily_Swing"].max()
                min_swing = prices_df["Daily_Swing"].min()
                std_swing = prices_df["Daily_Swing"].std()

                # Consistency: % of days with above-average swings
                avg_all = prices_df["Daily_Swing"].mean()
                consistent_days = len(prices_df[prices_df["Daily_Swing"] > avg_all])
                consistency_score = (consistent_days / len(prices_df) * 100) if len(prices_df) > 0 else 0

                # Volatility coefficient (std dev / mean)
                volatility_coeff = (std_swing / avg_swing) if avg_swing > 0 else 0

                # Volume check
                avg_volume = prices_df["Volume"].mean()
                min_volume_threshold = min_volume_filter * 1e6

                # Recent trend
                recent_5_avg = prices_df["Close"].tail(5).mean()
                older_5_avg = prices_df["Close"].iloc[0:5].mean() if len(prices_df) >= 5 else prices_df["Close"].iloc[0]
                trend_direction = "UP" if recent_5_avg > older_5_avg else "DOWN"

                # Swing trading score (0-100)
                score = 0
                score += min(40, avg_swing_pct * 4)  # Volatility (max 40 points)
                score += min(30, consistency_score / 2)  # Consistency (max 30 points)
                score += min(20, (avg_volume / min_volume_threshold) * 20) if avg_volume > 0 else 0  # Liquidity (max 20 points)
                score += 10 if volatility_coeff > 1.5 else 5  # Extra volatility bonus

                latest_price = prices_df["Close"].iloc[-1]
                latest_swing = prices_df["Daily_Swing"].iloc[-1]
                today_direction = "UP" if prices_df["Close"].iloc[-1] > prices_df["Open"].iloc[-1] else "DOWN"

                # Only include if passes minimum volume filter
                if avg_volume >= min_volume_threshold:
                    swing_data.append({
                        "Ticker": ticker,
                        "Price": latest_price,
                        "Swing Score": score,
                        "Avg Swing $": avg_swing,
                        "Avg Swing %": avg_swing_pct,
                        "Today Swing": latest_swing,
                        "Consistency %": consistency_score,
                        "Volatility": volatility_coeff,
                        "Avg Volume M": avg_volume / 1e6,
                        "Trend": trend_direction,
                        "Today": today_direction,
                        "Max Swing": max_swing,
                        "Min Swing": min_swing,
                    })
        except Exception as e:
            continue

    if swing_data:
        swing_df = pd.DataFrame(swing_data)
        swing_df = swing_df.sort_values("Swing Score", ascending=False)

        # Top opportunities
        st.markdown("### 🚀 Top Swing Trading Opportunities")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            top_score = swing_df["Swing Score"].max()
            st.metric("Best Score", f"{top_score:.0f}/100")
        with col2:
            avg_avg_swing = swing_df["Avg Swing %"].mean()
            st.metric("Portfolio Avg Swing", f"{avg_avg_swing:.2f}%")
        with col3:
            high_volatility = len(swing_df[swing_df["Volatility"] > 1.5])
            st.metric("High Volatility Stocks", high_volatility)
        with col4:
            consistent = len(swing_df[swing_df["Consistency %"] > 70])
            st.metric("Highly Consistent", consistent)

        st.divider()

        # Display top 20 opportunities
        display_df = swing_df.head(20)[
            ["Ticker", "Price", "Swing Score", "Avg Swing %", "Consistency %", "Trend", "Today", "Avg Volume M"]
        ].copy()
        display_df["Price"] = display_df["Price"].apply(lambda x: f"${x:.2f}")
        display_df["Swing Score"] = display_df["Swing Score"].apply(lambda x: f"{x:.0f}")
        display_df["Avg Swing %"] = display_df["Avg Swing %"].apply(lambda x: f"{x:.2f}%")
        display_df["Consistency %"] = display_df["Consistency %"].apply(lambda x: f"{x:.1f}%")
        display_df["Avg Volume M"] = display_df["Avg Volume M"].apply(lambda x: f"{x:.1f}M")

        st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.markdown("**Legend:** 🔴 RED = Price went DOWN | 🟢 GREEN = Price went UP")

        # Charts
        st.divider()
        st.markdown("### 📊 Analysis Charts")

        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            chart_data = swing_df.head(15)
            fig = px.bar(
                chart_data,
                x="Ticker",
                y="Swing Score",
                title="Top 15 Swing Trading Scores",
                color="Swing Score",
                color_continuous_scale="Viridis"
            )
            fig.update_yaxes(range=[0, 100])
            st.plotly_chart(fig, use_container_width=True)

        with col_chart2:
            chart_data = swing_df.head(15)
            fig = px.scatter(
                chart_data,
                x="Avg Swing %",
                y="Consistency %",
                size="Avg Volume M",
                color="Swing Score",
                hover_data=["Ticker"],
                title="Volatility vs Consistency (size = volume)",
                labels={"Avg Swing %": "Average Daily Swing %", "Consistency %": "Profitable Days %"}
            )
            st.plotly_chart(fig, use_container_width=True)

        # Open → High Opportunity Table
        st.divider()
        st.markdown("### 📈 Open → High Opportunity Analysis")
        st.markdown(
            "Average daily upside from **Open to High** across multiple lookback windows. "
            "Shows which stocks consistently offer the largest intraday move from the opening price."
        )

        opp_data = []
        for ticker in filtered_tickers:
            try:
                prices = db.get_daily_prices(ticker, days=30)
                if prices and len(prices) >= 5:
                    odf = pd.DataFrame(
                        prices,
                        columns=["Date", "Open", "Close", "High", "Low", "Volume"]
                    )
                    odf = odf.sort_values("Date")
                    odf["H_vs_O_pct"] = (odf["High"] - odf["Open"]) / odf["Open"] * 100
                    odf["H_vs_O_usd"] = odf["High"] - odf["Open"]

                    row = {
                        "Ticker": ticker,
                        "Company": TICKER_NAMES.get(ticker, ticker),
                        "Last Price": odf["Close"].iloc[-1],
                    }
                    for window in [5, 10, 15, 20, 25, 30]:
                        pct_tail = odf["H_vs_O_pct"].tail(window)
                        usd_tail = odf["H_vs_O_usd"].tail(window)
                        has_data = len(pct_tail) >= window
                        row[f"{window}D Avg $"] = round(usd_tail.mean(), 3) if has_data else None
                        row[f"{window}D Avg %"] = round(pct_tail.mean(), 3) if has_data else None

                    # Identify the window that produced the highest average opportunity
                    window_cols = [f"{w}D Avg %" for w in [5, 10, 15, 20, 25, 30]]
                    valid = {k: row[k] for k in window_cols if row[k] is not None}
                    if valid:
                        row["Best Window"] = max(valid, key=valid.get)
                        best_w = row["Best Window"].replace("Avg %", "Avg $")
                        row["Peak Avg $"] = row.get(best_w)
                        row["Peak Avg %"] = max(valid.values())
                    else:
                        row["Best Window"] = "N/A"
                        row["Peak Avg $"] = None
                        row["Peak Avg %"] = None

                    opp_data.append(row)
            except Exception:
                continue

        if opp_data:
            # Build ordered columns: interleave $ and % for each window
            window_cols_ordered = []
            for w in [5, 10, 15, 20, 25, 30]:
                window_cols_ordered += [f"{w}D Avg $", f"{w}D Avg %"]

            opp_df = pd.DataFrame(opp_data).sort_values("30D Avg %", ascending=False).reset_index(drop=True)
            opp_df.insert(0, "Rank", range(1, len(opp_df) + 1))
            opp_df = opp_df[["Rank", "Ticker", "Company", "Last Price"] + window_cols_ordered + ["Best Window", "Peak Avg $", "Peak Avg %"]]

            opp_display = opp_df.copy()
            opp_display["Last Price"] = opp_display["Last Price"].apply(lambda x: f"${x:.2f}")
            for w in [5, 10, 15, 20, 25, 30]:
                opp_display[f"{w}D Avg $"] = opp_display[f"{w}D Avg $"].apply(
                    lambda x: f"${x:.2f}" if pd.notna(x) else "N/A"
                )
                opp_display[f"{w}D Avg %"] = opp_display[f"{w}D Avg %"].apply(
                    lambda x: f"{x:.2f}%" if pd.notna(x) else "N/A"
                )
            opp_display["Peak Avg $"] = opp_display["Peak Avg $"].apply(
                lambda x: f"${x:.2f}" if pd.notna(x) else "N/A"
            )
            opp_display["Peak Avg %"] = opp_display["Peak Avg %"].apply(
                lambda x: f"{x:.2f}%" if pd.notna(x) else "N/A"
            )

            st.dataframe(opp_display, use_container_width=True, hide_index=True)
            st.caption("Ranked by 30-day average. 'Best Window' shows which lookback had the highest avg Open→High move.")

        # Detailed Analysis
        st.divider()
        st.markdown("### 🎯 Detailed Stock Analysis")

        selected_swing_ticker = st.selectbox(
            "Select stock for detailed swing analysis",
            swing_df["Ticker"].head(20),
            key="swing_ticker",
            format_func=lambda t: f"{TICKER_NAMES.get(t, t)} ({t})"
        )

        if selected_swing_ticker:
            stock_data = swing_df[swing_df["Ticker"] == selected_swing_ticker].iloc[0]

            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Current Price", f"${stock_data['Price']:.2f}")
            with col2:
                st.metric("Avg Daily Swing", f"${stock_data['Avg Swing $']:.2f}")
            with col3:
                st.metric("Avg Swing %", f"{stock_data['Avg Swing %']:.2f}%")
            with col4:
                st.metric("Consistency", f"{stock_data['Consistency %']:.1f}%")
            with col5:
                st.metric("Volatility Index", f"{stock_data['Volatility']:.2f}")

            # Get detailed daily data
            prices = db.get_daily_prices(selected_swing_ticker, days=swing_days)
            if prices:
                detail_df = pd.DataFrame(
                    prices,
                    columns=["Date", "Open", "Close", "High", "Low", "Volume"]
                )
                detail_df = detail_df.sort_values("Date")
                detail_df["Swing"] = abs(detail_df["Close"] - detail_df["Open"])
                detail_df["Swing %"] = (detail_df["Swing"] / detail_df["Open"] * 100)
                detail_df["Direction"] = detail_df["Close"] - detail_df["Open"]
                detail_df["Range"] = detail_df["High"] - detail_df["Low"]

                # Display daily data
                st.markdown(f"#### Daily Swing Data for {selected_swing_ticker}")
                display_detail = detail_df.tail(15)[
                    ["Date", "Open", "Close", "Swing", "Swing %", "Direction", "High", "Low", "Volume"]
                ].copy()

                display_detail["Open"] = display_detail["Open"].apply(lambda x: f"${x:.2f}")
                display_detail["Close"] = display_detail["Close"].apply(lambda x: f"${x:.2f}")
                display_detail["High"] = display_detail["High"].apply(lambda x: f"${x:.2f}")
                display_detail["Low"] = display_detail["Low"].apply(lambda x: f"${x:.2f}")
                display_detail["Swing"] = display_detail["Swing"].apply(lambda x: f"${x:.2f}")
                display_detail["Swing %"] = display_detail["Swing %"].apply(lambda x: f"{x:.2f}%")
                display_detail["Direction"] = display_detail["Direction"].apply(lambda x: f"${x:+.2f}")
                display_detail["Volume"] = display_detail["Volume"].apply(lambda x: f"{x/1e6:.1f}M")

                st.dataframe(display_detail, use_container_width=True, hide_index=True)

                # Trading signals
                st.markdown(f"#### 🎯 Trading Signals for {selected_swing_ticker}")

                latest_close = detail_df["Close"].iloc[-1]
                latest_open = detail_df["Open"].iloc[-1]
                avg_swing_val = detail_df["Swing"].mean()

                # Support/Resistance levels (simple approach)
                support = detail_df["Low"].tail(5).min()
                resistance = detail_df["High"].tail(5).max()

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Support Level", f"${support:.2f}")
                with col2:
                    st.metric("Current Price", f"${latest_close:.2f}")
                with col3:
                    st.metric("Resistance Level", f"${resistance:.2f}")

                st.markdown(f"""
                **Trading Strategy:**
                - **Buy Signal:** Price near support (${support:.2f}) with avg swing ${avg_swing_val:.2f}
                - **Target:** Resistance at ${resistance:.2f}
                - **Stop Loss:** Below ${support - avg_swing_val:.2f}
                - **Expected Swing:** ${avg_swing_val:.2f} ({stock_data['Avg Swing %']:.2f}%) per day
                - **Trend:** {stock_data['Trend']}
                - **Consistency:** {stock_data['Consistency %']:.1f}% of days profitable
                """)

    else:
        st.warning("No stocks meet the volume filter criteria. Please adjust the minimum volume threshold.")


# TAB 9: DAILY PRICE LOG - AGGREGATED PRICE DATA WITH CSV EXPORT
with tab9:
    st.subheader("Daily Price Log")
    st.markdown("Historical price data with Previous Close, Open, High, Low, and 52-Week Range")

    col1, col2 = st.columns([2, 1])
    with col1:
        log_ticker = st.selectbox(
            "Select Stock", filtered_tickers, key="price_log_ticker",
            format_func=lambda t: f"{TICKER_NAMES.get(t, t)} ({t})"
        )
    with col2:
        st.write("")
        if st.button("🔄 Refresh Data", key="refresh_log"):
            st.rerun()

    if log_ticker:
        # Get company name
        log_company_name = TICKER_NAMES.get(log_ticker, log_ticker)
        log_display_name = f"{log_company_name} - {log_ticker}"

        # Get 365 days of data for 52-week range calculation
        all_prices = db.get_daily_prices(log_ticker, days=365)

        # Get last 30 days for detailed view
        recent_prices = db.get_daily_prices(log_ticker, days=30)

        if recent_prices and len(recent_prices) > 0:
            recent_df = pd.DataFrame(
                recent_prices,
                columns=["Date", "Open", "Close", "High", "Low", "Volume"]
            )
            recent_df = recent_df.sort_values("Date")
            recent_df["Day's Range"] = recent_df["High"] - recent_df["Low"]

            # Calculate 52-week range from all available data
            if all_prices and len(all_prices) > 0:
                all_df = pd.DataFrame(
                    all_prices,
                    columns=["Date", "Open", "Close", "High", "Low", "Volume"]
                )
                week_52_high = all_df["High"].max()
                week_52_low = all_df["Low"].min()
            else:
                week_52_high = recent_df["High"].max()
                week_52_low = recent_df["Low"].min()

            # Build display dataframe
            display_log = recent_df.copy()
            display_log["Previous Close"] = display_log["Close"].shift(1)
            display_log["Day's Range"] = display_log["High"] - display_log["Low"]
            display_log["52W High"] = week_52_high
            display_log["52W Low"] = week_52_low
            display_log["52W Range"] = week_52_high - week_52_low

            # Intraday growth metrics
            display_log["High vs Open %"] = (display_log["High"] - display_log["Open"]) / display_log["Open"] * 100
            display_log["Close vs Open %"] = (display_log["Close"] - display_log["Open"]) / display_log["Open"] * 100

            # Reorder columns for display
            display_log = display_log[[
                "Date", "Previous Close", "High", "Open", "Low", "Close",
                "High vs Open %", "Close vs Open %",
                "Day's Range", "52W High", "52W Low", "52W Range", "Volume"
            ]]

            # Format for display
            log_display = display_log.copy()
            log_display["Date"] = log_display["Date"].astype(str)
            log_display["Previous Close"] = log_display["Previous Close"].apply(lambda x: f"${x:.2f}" if pd.notna(x) else "N/A")
            log_display["High"] = log_display["High"].apply(lambda x: f"${x:.2f}")
            log_display["Open"] = log_display["Open"].apply(lambda x: f"${x:.2f}")
            log_display["Low"] = log_display["Low"].apply(lambda x: f"${x:.2f}")
            log_display["Close"] = log_display["Close"].apply(lambda x: f"${x:.2f}")
            log_display["High vs Open %"] = log_display["High vs Open %"].apply(lambda x: f"▲ +{x:.2f}%")
            log_display["Close vs Open %"] = log_display["Close vs Open %"].apply(
                lambda x: f"▲ +{x:.2f}%" if x >= 0 else f"▼ {x:.2f}%"
            )
            log_display["Day's Range"] = log_display["Day's Range"].apply(lambda x: f"${x:.2f}")
            log_display["52W High"] = log_display["52W High"].apply(lambda x: f"${x:.2f}")
            log_display["52W Low"] = log_display["52W Low"].apply(lambda x: f"${x:.2f}")
            log_display["52W Range"] = log_display["52W Range"].apply(lambda x: f"${x:.2f}")
            log_display["Volume"] = log_display["Volume"].apply(lambda x: f"{int(x/1e6)}M" if x > 1e6 else f"{int(x/1e3)}K")

            # Display metrics
            st.divider()
            col1, col2, col3, col4, col5 = st.columns(5)

            current_price = recent_df["Close"].iloc[-1]
            prev_close = recent_df["Close"].iloc[-2] if len(recent_df) > 1 else current_price
            price_change = current_price - prev_close
            price_change_pct = (price_change / prev_close * 100) if prev_close > 0 else 0

            with col1:
                st.metric(f"{log_display_name} Current", f"${current_price:.2f}")
            with col2:
                st.metric("Previous Close", f"${prev_close:.2f}")
            with col3:
                st.metric("Day Change", f"${price_change:+.2f} ({price_change_pct:+.2f}%)")
            with col4:
                st.metric("52W High", f"${week_52_high:.2f}")
            with col5:
                st.metric("52W Low", f"${week_52_low:.2f}")

            st.divider()

            # Display the data table
            st.subheader(f"Last 30 Days Price Data - {log_display_name}")
            st.dataframe(
                log_display.sort_values("Date", ascending=False),
                use_container_width=True,
                hide_index=True,
                height=600
            )

            # CSV Export
            st.divider()
            st.subheader("📥 Export Data")

            # Convert to CSV
            csv_data = display_log.sort_values("Date", ascending=False).copy()
            csv_data["Date"] = csv_data["Date"].astype(str)
            csv_buffer = csv_data.to_csv(index=False)

            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write("Download your daily price log as CSV file")
            with col2:
                st.write("")
            with col3:
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_buffer,
                    file_name=f"{log_ticker}_daily_prices.csv",
                    mime="text/csv"
                )

            # Data insights
            st.divider()
            st.subheader("📈 30-Day Insights")

            col1, col2, col3, col4 = st.columns(4)

            daily_range = recent_df["High"] - recent_df["Low"]
            avg_daily_range = daily_range.mean()
            max_daily_range = daily_range.max()
            min_daily_range = daily_range.min()
            avg_volume = recent_df["Volume"].mean()

            with col1:
                st.metric("Avg Daily Range", f"${avg_daily_range:.2f}")
            with col2:
                st.metric("Max Daily Range", f"${max_daily_range:.2f}")
            with col3:
                st.metric("Min Daily Range", f"${min_daily_range:.2f}")
            with col4:
                st.metric("Avg Volume", f"{avg_volume/1e6:.1f}M")

            # Price trend chart
            fig = px.line(
                recent_df,
                x="Date",
                y="Close",
                title=f"{log_display_name} - 30 Day Price Trend",
                markers=True
            )
            fig.add_trace(
                go.Scatter(
                    x=recent_df["Date"],
                    y=recent_df["High"],
                    mode="lines",
                    name="High",
                    line=dict(dash="dash", color="green")
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=recent_df["Date"],
                    y=recent_df["Low"],
                    mode="lines",
                    name="Low",
                    line=dict(dash="dash", color="red")
                )
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info(f"No price data available for {log_ticker}. Please ensure backfill_history.py has been run.")
