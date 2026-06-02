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
from config import TICKERS, ALL_TICKERS

# Page configuration
st.set_page_config(
    page_title="Stocks Management Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
db = DatabaseManager()

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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Signals",
    "💼 Portfolio",
    "📊 Performance",
    "🔍 Fundamentals",
    "📅 Historical"
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
                st.dataframe(
                    buy_signals[["Ticker", "Reason", "Strength", "Date"]],
                    use_container_width=True,
                    hide_index=True
                )

        with col2:
            sell_signals = signals_df[signals_df["Signal Type"] == "SELL"].head(10)
            if not sell_signals.empty:
                st.subheader("🔴 Sell Signals")
                st.dataframe(
                    sell_signals[["Ticker", "Reason", "Strength", "Date"]],
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
            performance_data.append({
                "Ticker": ticker,
                "Price": fund[2],
                "PE Ratio": fund[3],
                "Dividend Yield %": fund[4],
                "EPS": fund[9]
            })

    if performance_data:
        perf_df = pd.DataFrame(performance_data)

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

    selected_ticker = st.selectbox("Select Stock", filtered_tickers)

    if selected_ticker:
        fund = db.get_latest_fundamentals(selected_ticker)

        if fund:
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Price", f"${fund[2]:.2f}" if fund[2] else "N/A")

            with col2:
                st.metric("PE Ratio", f"{fund[3]:.2f}" if fund[3] else "N/A")

            with col3:
                st.metric("Dividend Yield", f"{fund[4]:.2f}%" if fund[4] else "N/A")

            with col4:
                st.metric("EPS", f"${fund[9]:.2f}" if fund[9] else "N/A")

            st.divider()

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Market Cap", f"${fund[5]/1e9:.2f}B" if fund[5] else "N/A")
                st.metric("Revenue", f"${fund[6]/1e9:.2f}B" if fund[6] else "N/A")

            with col2:
                st.metric("Net Income", f"${fund[7]/1e9:.2f}B" if fund[7] else "N/A")
                st.metric("Book Value", f"${fund[8]:.2f}" if fund[8] else "N/A")

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

    selected_ticker = st.selectbox("Select Stock for Historical Analysis", filtered_tickers, key="history_ticker")
    days_lookback = st.slider("Days to Display", 30, 365, 90)

    if selected_ticker:
        prices = db.get_daily_prices(selected_ticker, days=days_lookback)

        if prices:
            prices_df = pd.DataFrame(
                prices,
                columns=["Date", "Open", "Close", "High", "Low", "Volume"]
            )
            prices_df = prices_df.sort_values("Date")

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
                title=f"{selected_ticker} - Historical Price Data",
                height=500,
                xaxis_rangeslider_visible=False
            )
            st.plotly_chart(fig, use_container_width=True)

            # Volume analysis
            fig = px.bar(prices_df, x="Date", y="Volume", title=f"{selected_ticker} - Trading Volume")
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

            # Display data table
            st.subheader("Data Table")
            st.dataframe(prices_df, use_container_width=True, hide_index=True)
        else:
            st.info(f"No historical data available for {selected_ticker}")
