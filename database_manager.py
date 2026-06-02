"""
SQLite Database Manager for Stock Portfolio
"""

import sqlite3
import os
from datetime import datetime
from config import DB_PATH


class DatabaseManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_database()

    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)

    def init_database(self):
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Stocks table - fundamentals
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stocks (
                id INTEGER PRIMARY KEY,
                ticker TEXT UNIQUE NOT NULL,
                name TEXT,
                sector TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Daily prices and performance
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_prices (
                id INTEGER PRIMARY KEY,
                ticker TEXT NOT NULL,
                date DATE NOT NULL,
                open REAL,
                close REAL,
                high REAL,
                low REAL,
                volume INTEGER,
                UNIQUE(ticker, date),
                FOREIGN KEY(ticker) REFERENCES stocks(ticker)
            )
        """)

        # Fundamentals snapshot
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fundamentals (
                id INTEGER PRIMARY KEY,
                ticker TEXT NOT NULL,
                date DATE NOT NULL,
                price REAL,
                pe_ratio REAL,
                dividend_yield REAL,
                market_cap REAL,
                revenue REAL,
                net_income REAL,
                book_value REAL,
                eps REAL,
                UNIQUE(ticker, date),
                FOREIGN KEY(ticker) REFERENCES stocks(ticker)
            )
        """)

        # Earnings data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS earnings (
                id INTEGER PRIMARY KEY,
                ticker TEXT NOT NULL,
                quarter TEXT,
                eps_estimate REAL,
                eps_actual REAL,
                revenue_estimate REAL,
                revenue_actual REAL,
                surprise_percent REAL,
                date DATE,
                FOREIGN KEY(ticker) REFERENCES stocks(ticker)
            )
        """)

        # Portfolio holdings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY,
                ticker TEXT NOT NULL UNIQUE,
                shares_owned REAL,
                average_cost REAL,
                date_added DATE,
                FOREIGN KEY(ticker) REFERENCES stocks(ticker)
            )
        """)

        # Buy/Sell signals
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY,
                ticker TEXT NOT NULL,
                signal_type TEXT,  -- 'BUY', 'SELL', 'HOLD'
                signal_reason TEXT,  -- 'dividend_yield', 'moving_average', 'earnings'
                strength REAL,  -- 0-100 score
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(ticker) REFERENCES stocks(ticker)
            )
        """)

        conn.commit()
        conn.close()

    def insert_stock(self, ticker, name, sector):
        """Insert a new stock"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT OR REPLACE INTO stocks (ticker, name, sector) VALUES (?, ?, ?)",
                (ticker, name, sector)
            )
            conn.commit()
        except Exception as e:
            print(f"Error inserting stock {ticker}: {e}")
        finally:
            conn.close()

    def insert_daily_prices(self, ticker, date, open_price, close, high, low, volume):
        """Insert daily price data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO daily_prices
                (ticker, date, open, close, high, low, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (ticker, date, open_price, close, high, low, volume))
            conn.commit()
        except Exception as e:
            print(f"Error inserting prices for {ticker}: {e}")
        finally:
            conn.close()

    def insert_fundamentals(self, ticker, date, price, pe_ratio, dividend_yield,
                           market_cap, revenue, net_income, book_value, eps):
        """Insert fundamental data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO fundamentals
                (ticker, date, price, pe_ratio, dividend_yield, market_cap, revenue, net_income, book_value, eps)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (ticker, date, price, pe_ratio, dividend_yield, market_cap, revenue, net_income, book_value, eps))
            conn.commit()
        except Exception as e:
            print(f"Error inserting fundamentals for {ticker}: {e}")
        finally:
            conn.close()

    def insert_signal(self, ticker, signal_type, signal_reason, strength):
        """Insert buy/sell signal"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO signals (ticker, signal_type, signal_reason, strength)
                VALUES (?, ?, ?, ?)
            """, (ticker, signal_type, signal_reason, strength))
            conn.commit()
        except Exception as e:
            print(f"Error inserting signal for {ticker}: {e}")
        finally:
            conn.close()

    def get_daily_prices(self, ticker, days=252):
        """Get recent daily prices"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date, open, close, high, low, volume
            FROM daily_prices
            WHERE ticker = ?
            ORDER BY date DESC
            LIMIT ?
        """, (ticker, days))
        return cursor.fetchall()

    def get_latest_fundamentals(self, ticker):
        """Get latest fundamental data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM fundamentals
            WHERE ticker = ?
            ORDER BY date DESC
            LIMIT 1
        """, (ticker,))
        return cursor.fetchone()

    def get_all_stocks(self):
        """Get all stocks in database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ticker, name, sector FROM stocks")
        return cursor.fetchall()

    def get_latest_signals(self, days=7):
        """Get recent signals"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ticker, signal_type, signal_reason, strength, date
            FROM signals
            WHERE date >= datetime('now', '-' || ? || ' days')
            ORDER BY date DESC
        """, (days,))
        return cursor.fetchall()

    def get_portfolio(self):
        """Get portfolio holdings"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ticker, shares_owned, average_cost, date_added FROM portfolio")
        return cursor.fetchall()

    def update_portfolio(self, ticker, shares_owned, average_cost):
        """Update portfolio holdings"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO portfolio (ticker, shares_owned, average_cost, date_added)
                VALUES (?, ?, ?, DATE('now'))
            """, (ticker, shares_owned, average_cost))
            conn.commit()
        except Exception as e:
            print(f"Error updating portfolio for {ticker}: {e}")
        finally:
            conn.close()
