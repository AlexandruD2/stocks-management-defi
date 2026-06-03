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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Signals",
    "💼 Portfolio",
    "📊 Performance",
    "🔍 Fundamentals",
    "📅 Historical",
    "📉 Volatility"
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

    selected_ticker = st.selectbox("Select Stock", filtered_tickers)

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
        days_range = st.slider("Days of History", 5, 90, 30)
    with col2:
        st.write("")
    with col3:
        st.write("")

    if selected_stocks:
        st.divider()

        # Create combined analysis for all selected stocks
        all_volatility_data = []

        for ticker in selected_stocks:
            prices = db.get_daily_prices(ticker, days=days_range)

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
            st.markdown("### Detailed OHLC Data")

            with st.expander("Show detailed data tables"):
                for ticker in selected_stocks:
                    ticker_data = combined_df[combined_df["Ticker"] == ticker].copy()

                    if not ticker_data.empty:
                        st.markdown(f"**{ticker}**")

                        # Display clean table
                        display_df = ticker_data[[
                            "Date", "Open", "High", "Low", "Close",
                            "Daily_Change_Pct", "Volatility_Pct", "Volume"
                        ]].copy()

                        display_df = display_df.rename(columns={
                            "Daily_Change_Pct": "Change %",
                            "Volatility_Pct": "Vol %",
                            "Volume": "Vol"
                        })

                        # Format for display
                        display_df["Open"] = display_df["Open"].apply(lambda x: f"${x:.2f}")
                        display_df["High"] = display_df["High"].apply(lambda x: f"${x:.2f}")
                        display_df["Low"] = display_df["Low"].apply(lambda x: f"${x:.2f}")
                        display_df["Close"] = display_df["Close"].apply(lambda x: f"${x:.2f}")
                        display_df["Change %"] = display_df["Change %"].apply(lambda x: f"{x:+.2f}%")
                        display_df["Vol %"] = display_df["Vol %"].apply(lambda x: f"{x:.2f}%")
                        display_df["Vol"] = display_df["Vol"].apply(lambda x: f"{int(x/1e6):.1f}M" if x > 1e6 else f"{int(x/1e3):.0f}K")

                        st.dataframe(
                            display_df.sort_values("Date", ascending=False),
                            use_container_width=True,
                            hide_index=True
                        )
    else:
        st.info("👆 Click a preset or select stocks above to get started!")
