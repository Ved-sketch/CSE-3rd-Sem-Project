"""
Finsight - Financial Intelligence Hub
Main Application File
"""

import time
import customtkinter as ctk
import requests
import threading
import re
from urllib.parse import urlparse
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import math

# Import configuration
from config import COLORS

# Import custom modules
from sip_calculator import SIPCalculator
from currency_converter import CurrencyConverter

ctk.set_appearance_mode("Light")  # Force light mode for purple theme
ctk.set_default_color_theme("blue")
ctk.set_window_scaling(1.0)
ctk.set_widget_scaling(1.0)


class GUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Finsight - Enhanced Financial Hub")
        
        # Initialize news articles list for better refresh handling
        self.news_articles = []

        # centring the app
        self.centring_the_app()
        
        # Create navigation frame
        self.create_navigation()

        # Main content frame
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.pack(pady=(0, 10), padx=10, fill="both", expand=True)

        # Show dashboard by default
        self.show_dashboard()

        self.root.mainloop()
    
    def create_navigation(self):
        """Create navigation bar"""
        nav_frame = ctk.CTkFrame(self.root, height=60)
        nav_frame.pack(pady=10, padx=10, fill="x")
        nav_frame.pack_propagate(False)
        
        # App title
        title_label = ctk.CTkLabel(
            nav_frame,
            text="📊 Finsight",
            font=("Arial", 20, "bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        title_label.pack(side="left", padx=20, pady=15)
        
        # Navigation buttons
        nav_buttons_frame = ctk.CTkFrame(nav_frame, fg_color="transparent")
        nav_buttons_frame.pack(side="right", padx=20, pady=10)
        
        self.dashboard_btn = ctk.CTkButton(
            nav_buttons_frame,
            text="🏠 Dashboard",
            command=self.show_dashboard,
            width=120,
            height=35
        )
        self.dashboard_btn.pack(side="left", padx=5)
        
        self.sip_btn = ctk.CTkButton(
            nav_buttons_frame,
            text="🧮 SIP Calculator",
            command=self.show_sip_calculator,
            width=120,
            height=35
        )
        self.sip_btn.pack(side="left", padx=5)
        
        self.currency_btn = ctk.CTkButton(
            nav_buttons_frame,
            text="💱 Currency",
            command=self.show_currency_converter,
            width=120,
            height=35
        )
        self.currency_btn.pack(side="left", padx=5)
    
    def clear_content(self):
        """Clear current content"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show main dashboard"""
        self.clear_content()
        
        # Update button states
        self.dashboard_btn.configure(state="disabled")
        self.sip_btn.configure(state="normal")
        self.currency_btn.configure(state="normal")
        
        # Create scrollable main frame
        self.main_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            orientation="vertical",
            corner_radius=15
        )
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.greeting()
        self.create_stock_widgets()
        self.load_news()
    
    def show_sip_calculator(self):
        """Show SIP Calculator"""
        self.clear_content()
        
        # Update button states
        self.dashboard_btn.configure(state="normal")
        self.sip_btn.configure(state="disabled")
        self.currency_btn.configure(state="normal")
        
        # Create SIP calculator
        sip_calculator = SIPCalculator(self.content_frame)
        sip_calculator.pack(fill="both", expand=True, padx=10, pady=10)
    
    def show_currency_converter(self):
        """Show Currency Converter"""
        self.clear_content()
        
        # Update button states
        self.dashboard_btn.configure(state="normal")
        self.sip_btn.configure(state="normal")
        self.currency_btn.configure(state="disabled")
        
        # Create currency converter
        currency_converter = CurrencyConverter(self.content_frame)
        currency_converter.pack(fill="both", expand=True, padx=10, pady=10)

    def greeting(self):
        current_time = time.strftime("%H:%M")
        if current_time > "06:00" and current_time < "12:00":
            message = "Good Morning!"
        elif current_time > '12:00' and current_time < '19:00':
            message = "Good Afternoon"
        else:
            message = "Working Late?"
        
        label = ctk.CTkLabel(self.main_frame, text=message, font=("Times New Roman", 22))
        label.pack(pady=30)
        
        # Add Finsight subtitle
        subtitle = ctk.CTkLabel(
            self.main_frame, 
            text="Welcome to Finsight - Your Complete Financial Intelligence Hub 📊", 
            font=("Arial", 16),
            text_color=("#2563eb", "#3b82f6")
        )
        subtitle.pack(pady=(0, 20))

    def create_stock_widgets(self):
        """Create stock price widgets and market charts"""
        # Create main container for financial widgets
        financial_container = ctk.CTkFrame(self.main_frame, corner_radius=15)
        financial_container.pack(pady=20, padx=20, fill="x")
        
        # Title for financial section
        finance_title = ctk.CTkLabel(
            financial_container, 
            text="📈 Live Market Data & Charts", 
            font=("Arial", 18, "bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        finance_title.pack(pady=(15, 10))
        
        # Create market summary
        self.create_market_summary(financial_container)
        
        # Create stock price widgets frame
        self.create_stock_price_widgets(financial_container)
        
        # Create market chart
        self.create_market_chart(financial_container)

    def create_market_summary(self, parent):
        """Create market summary with major indices"""
        summary_frame = ctk.CTkFrame(parent, corner_radius=10)
        summary_frame.pack(pady=10, padx=15, fill="x")
        
        summary_title = ctk.CTkLabel(
            summary_frame,
            text="🏛️ Market Indices",
            font=("Arial", 16, "bold")
        )
        summary_title.pack(pady=(10, 5))
        
        # Create indices grid
        indices_grid = ctk.CTkFrame(summary_frame, fg_color="transparent")
        indices_grid.pack(pady=10, padx=10, fill="x")
        
        # Major market indices
        indices = {
            "^GSPC": "S&P 500",
            "^DJI": "Dow Jones",
            "^IXIC": "NASDAQ"
        }
        
        self.index_widgets = {}
        for i, (symbol, name) in enumerate(indices.items()):
            # Create index widget
            index_widget = ctk.CTkFrame(indices_grid, corner_radius=8, width=240, height=70)
            index_widget.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
            index_widget.grid_propagate(False)
            
            # Index name
            name_label = ctk.CTkLabel(
                index_widget,
                text=name,
                font=("Arial", 12, "bold")
            )
            name_label.pack(pady=(8, 2))
            
            # Index value
            value_label = ctk.CTkLabel(
                index_widget,
                text="Loading...",
                font=("Arial", 11)
            )
            value_label.pack()
            
            # Index change
            change_label = ctk.CTkLabel(
                index_widget,
                text="",
                font=("Arial", 10)
            )
            change_label.pack(pady=(0, 8))
            
            self.index_widgets[symbol] = {
                'value_label': value_label,
                'change_label': change_label
            }
        
        # Configure grid weights
        for i in range(3):
            indices_grid.grid_columnconfigure(i, weight=1)
        
        # Load index data
        threading.Thread(target=self.load_index_data, daemon=True).start()

    def load_index_data(self):
        """Load market indices data"""
        try:
            for symbol in self.index_widgets.keys():
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="2d")
                    
                    if not hist.empty and len(hist) >= 2:
                        current_value = hist['Close'].iloc[-1]
                        prev_value = hist['Close'].iloc[-2]
                        change = current_value - prev_value
                        change_percent = (change / prev_value) * 100
                        
                        self.root.after(0, lambda s=symbol, v=current_value, c=change_percent:
                                       self.update_index_widget(s, v, c))
                        
                except Exception as e:
                    print(f"Error loading index {symbol}: {e}")
                    
        except Exception as e:
            print(f"Error in load_index_data: {e}")

    def update_index_widget(self, symbol, value, change_percent):
        """Update market index widget"""
        if symbol in self.index_widgets:
            widget_info = self.index_widgets[symbol]
            
            # Update value
            value_text = f"{value:.2f}" if isinstance(value, (int, float)) else str(value)
            widget_info['value_label'].configure(text=value_text)
            
            # Update change
            if isinstance(change_percent, (int, float)):
                change_text = f"{change_percent:+.2f}%"
                color = ("#16a34a", "#22c55e") if change_percent > 0 else ("#dc2626", "#ef4444")
                arrow = "▲" if change_percent > 0 else "▼"
                widget_info['change_label'].configure(
                    text=f"{arrow} {change_text}",
                    text_color=color
                )

    def create_stock_price_widgets(self, parent):
        """Create live stock price widgets"""
        # Stock widgets container
        stock_container = ctk.CTkFrame(parent, corner_radius=10)
        stock_container.pack(pady=10, padx=15, fill="x")
        
        stock_title = ctk.CTkLabel(
            stock_container,
            text="💰 Popular Stocks",
            font=("Arial", 16, "bold")
        )
        stock_title.pack(pady=(10, 5))
        
        # Create a frame for stock widgets grid
        stocks_grid = ctk.CTkFrame(stock_container, fg_color="transparent")
        stocks_grid.pack(pady=10, padx=10, fill="x")
        
        # Popular stocks to display
        popular_stocks = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NVDA"]
        
        # Create stock widgets in a grid (3 columns, 2 rows)
        self.stock_widgets = {}
        for i, symbol in enumerate(popular_stocks):
            row = i // 3
            col = i % 3
            
            # Create individual stock widget
            stock_widget = ctk.CTkFrame(stocks_grid, corner_radius=8, width=220, height=80)
            stock_widget.grid(row=row, column=col, padx=8, pady=5, sticky="ew")
            stock_widget.grid_propagate(False)
            
            # Stock symbol
            symbol_label = ctk.CTkLabel(
                stock_widget,
                text=symbol,
                font=("Arial", 14, "bold"),
                text_color=("#1f538d", "#4a9eff")
            )
            symbol_label.pack(pady=(8, 2))
            
            # Price label (will be updated with real data)
            price_label = ctk.CTkLabel(
                stock_widget,
                text="Loading...",
                font=("Arial", 12)
            )
            price_label.pack()
            
            # Change label (will show percentage change)
            change_label = ctk.CTkLabel(
                stock_widget,
                text="",
                font=("Arial", 10)
            )
            change_label.pack(pady=(0, 8))
            
            self.stock_widgets[symbol] = {
                'price_label': price_label,
                'change_label': change_label,
                'widget': stock_widget
            }
        
        # Configure grid weights
        for i in range(3):
            stocks_grid.grid_columnconfigure(i, weight=1)
        
        # Load stock data in background
        threading.Thread(target=self.load_stock_data, daemon=True).start()
        
        # Add refresh button for stock data
        refresh_stocks_btn = ctk.CTkButton(
            stock_container,
            text="🔄 Refresh Stock Prices",
            command=self.refresh_stock_data,
            font=("Arial", 12),
            height=32,
            width=200
        )
        refresh_stocks_btn.pack(pady=(10, 15))

    def create_market_chart(self, parent):
        """Create market chart using matplotlib"""
        # Chart container
        chart_container = ctk.CTkFrame(parent, corner_radius=10)
        chart_container.pack(pady=15, padx=15, fill="both", expand=True)
        
        chart_title = ctk.CTkLabel(
            chart_container,
            text="📊 S&P 500 Chart (Last 30 Days)",
            font=("Arial", 16, "bold")
        )
        chart_title.pack(pady=(10, 5))
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.fig.patch.set_facecolor('#212121' if ctk.get_appearance_mode() == "Dark" else '#f0f0f0')
        
        # Initial placeholder chart
        self.ax.plot([1, 2, 3, 4, 5], [1, 4, 2, 3, 5], color='#4a9eff', linewidth=2)
        self.ax.set_title('Loading S&P 500 Data...', color='white' if ctk.get_appearance_mode() == "Dark" else 'black')
        self.ax.set_facecolor('#2b2b2b' if ctk.get_appearance_mode() == "Dark" else 'white')
        
        # Embed chart in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, chart_container)
        self.canvas.draw()
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Load chart data in background
        threading.Thread(target=self.load_chart_data, daemon=True).start()

    def load_stock_data(self):
        """Load real-time stock data"""
        try:
            for symbol in self.stock_widgets.keys():
                try:
                    # Get stock info
                    stock = yf.Ticker(symbol)
                    info = stock.info
                    hist = stock.history(period="2d")
                    
                    if not hist.empty and len(hist) >= 2:
                        current_price = hist['Close'].iloc[-1]
                        prev_price = hist['Close'].iloc[-2]
                        change = current_price - prev_price
                        change_percent = (change / prev_price) * 100
                        
                        # Update UI in main thread
                        self.root.after(0, lambda s=symbol, p=current_price, c=change_percent: 
                                       self.update_stock_widget(s, p, c))
                    else:
                        # Fallback to basic info
                        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                        if current_price:
                            self.root.after(0, lambda s=symbol, p=current_price: 
                                           self.update_stock_widget(s, p, 0))
                        
                except Exception as e:
                    print(f"Error loading {symbol}: {e}")
                    self.root.after(0, lambda s=symbol: self.update_stock_widget(s, "Error", 0))
                    
        except Exception as e:
            print(f"Error in load_stock_data: {e}")

    def update_stock_widget(self, symbol, price, change_percent):
        """Update individual stock widget with real data"""
        if symbol in self.stock_widgets:
            widget_info = self.stock_widgets[symbol]
            
            # Update price
            if isinstance(price, (int, float)):
                price_text = f"${price:.2f}"
                widget_info['price_label'].configure(text=price_text)
            else:
                widget_info['price_label'].configure(text=str(price))
            
            # Update change
            if isinstance(change_percent, (int, float)) and change_percent != 0:
                change_text = f"{change_percent:+.2f}%"
                color = ("#16a34a", "#22c55e") if change_percent > 0 else ("#dc2626", "#ef4444")
                arrow = "▲" if change_percent > 0 else "▼"
                widget_info['change_label'].configure(
                    text=f"{arrow} {change_text}",
                    text_color=color
                )
            else:
                widget_info['change_label'].configure(text="--")

    def load_chart_data(self):
        """Load S&P 500 chart data"""
        try:
            # Get S&P 500 data
            sp500 = yf.Ticker("^GSPC")
            hist = sp500.history(period="1mo")  # Last 30 days
            
            if not hist.empty:
                # Schedule chart update in main thread
                self.root.after(0, lambda: self.update_chart(hist))
            else:
                self.root.after(0, lambda: self.show_chart_error("No data available"))
                
        except Exception as e:
            self.root.after(0, lambda: self.show_chart_error(f"Error: {str(e)}"))

    def update_chart(self, data):
        """Update the market chart with real data"""
        try:
            # Clear previous plot
            self.ax.clear()
            
            # Set style based on appearance mode
            is_dark = ctk.get_appearance_mode() == "Dark"
            bg_color = '#2b2b2b' if is_dark else 'white'
            text_color = 'white' if is_dark else 'black'
            grid_color = '#404040' if is_dark else '#e0e0e0'
            
            self.ax.set_facecolor(bg_color)
            
            # Plot the closing prices
            dates = data.index
            closes = data['Close']
            
            # Create the line plot
            self.ax.plot(dates, closes, color='#4a9eff', linewidth=2.5, alpha=0.9)
            
            # Fill area under the curve
            self.ax.fill_between(dates, closes, alpha=0.2, color='#4a9eff')
            
            # Styling
            self.ax.set_title('S&P 500 Index - Last 30 Days', 
                            color=text_color, fontsize=14, fontweight='bold', pad=20)
            self.ax.set_xlabel('Date', color=text_color, fontsize=12)
            self.ax.set_ylabel('Price ($)', color=text_color, fontsize=12)
            
            # Grid
            self.ax.grid(True, alpha=0.3, color=grid_color)
            
            # Format axes
            self.ax.tick_params(colors=text_color, labelsize=10)
            
            # Format dates on x-axis
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
            self.ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
            
            # Rotate date labels
            plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            # Add current price annotation
            current_price = closes.iloc[-1]
            self.ax.annotate(f'${current_price:.2f}', 
                           xy=(dates[-1], current_price),
                           xytext=(10, 10), textcoords='offset points',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='#4a9eff', alpha=0.8),
                           color='white', fontweight='bold')
            
            # Tight layout
            self.fig.tight_layout()
            
            # Redraw canvas
            self.canvas.draw()
            
        except Exception as e:
            print(f"Error updating chart: {e}")
            self.show_chart_error(f"Chart update error: {str(e)}")

    def show_chart_error(self, error_msg):
        """Show error message on chart"""
        try:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"📊 Chart Error\n{error_msg}", 
                        transform=self.ax.transAxes, ha='center', va='center',
                        fontsize=12, color='red')
            self.ax.set_facecolor('#2b2b2b' if ctk.get_appearance_mode() == "Dark" else 'white')
            self.canvas.draw()
        except:
            pass

    def load_news(self):
        """Load financial news articles in a separate thread"""
        # Show loading message
        self.loading_label = ctk.CTkLabel(
            self.main_frame, 
            text="📈 Loading latest financial news & market updates...", 
            font=("Arial", 16),
            text_color=("#1f538d", "#4a9eff")
        )
        self.loading_label.pack(pady=15)
        
        # Fetch news in background thread to prevent UI freezing
        threading.Thread(target=self.fetch_and_display_news, daemon=True).start()

    def fetch_and_display_news(self):
        """Fetch financial/stock news from API and display in UI"""
        try:
            # Using MarketWatch RSS feed (verified working)
            marketwatch_url = "https://api.rss2json.com/v1/api.json?rss_url=https://feeds.marketwatch.com/marketwatch/realtimeheadlines/"
            
            response = requests.get(marketwatch_url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'ok':
                    # Schedule UI update in main thread
                    self.root.after(0, lambda: self.display_financial_news(data))
                else:
                    self.root.after(0, lambda: self.show_error("Failed to retrieve financial news data"))
            else:
                self.root.after(0, lambda: self.show_error(f"API returned status code: {response.status_code}"))
                
        except requests.exceptions.Timeout:
            self.root.after(0, lambda: self.show_error("Request timed out. Please check your internet connection."))
        except requests.exceptions.ConnectionError:
            self.root.after(0, lambda: self.show_error("Connection error. Please check your internet connection."))
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Error fetching financial news: {str(e)}"))

    def display_financial_news(self, data):
        """Display financial news articles in the UI"""
        # Remove loading message
        if hasattr(self, 'loading_label'):
            self.loading_label.destroy()
        
        # Add financial news header
        news_header = ctk.CTkLabel(
            self.main_frame, 
            text="📰 Latest Financial News & Market Updates", 
            font=("Arial", 20, "bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        news_header.pack(pady=(20, 10))
        self.news_articles.append(news_header)
        
        # Display news articles
        articles = data.get('items', [])[:8]  # Show top 8 financial articles
        
        for i, article in enumerate(articles):
            # Create frame for each article with financial styling
            article_frame = ctk.CTkFrame(
                self.main_frame, 
                corner_radius=12,
                border_width=1,
                border_color=("#d4d4d8", "#3f3f46")
            )
            article_frame.pack(pady=8, padx=15, fill="x")
            self.news_articles.append(article_frame)
            
            # Article title
            title = article.get('title', 'No title')
            # Clean up title
            if len(title) > 100:
                title = title[:100] + "..."
                
            title_label = ctk.CTkLabel(
                article_frame, 
                text=title, 
                font=("Arial", 15, "bold"),
                wraplength=720,
                justify="left",
                text_color=("#1a1a1a", "#ffffff")
            )
            title_label.pack(pady=(15, 8), padx=15, anchor="w")
            
            # Article description/content
            description = article.get('description', '') or article.get('content', '')
            if not description:
                description = "Click to read full article..."
            
            # Clean up description (remove HTML tags)
            description = re.sub(r'<[^>]+>', '', description)
            if len(description) > 200:
                description = description[:200] + "..."
                
            desc_label = ctk.CTkLabel(
                article_frame, 
                text=description, 
                font=("Arial", 13),
                wraplength=720,
                justify="left",
                text_color=("#4a5568", "#a0aec0")
            )
            desc_label.pack(pady=(0, 8), padx=15, anchor="w")
            
            # Create a frame for metadata (date, source, link)
            meta_frame = ctk.CTkFrame(article_frame, fg_color="transparent")
            meta_frame.pack(fill="x", padx=15, pady=(0, 15))
            
            # Publication date
            pub_date = article.get('pubDate', '')
            if pub_date:
                try:
                    # Handle different date formats
                    if 'T' in pub_date:
                        date_obj = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                    else:
                        date_obj = datetime.strptime(pub_date[:19], "%Y-%m-%d %H:%M:%S")
                    
                    formatted_date = date_obj.strftime("%b %d, %Y • %I:%M %p")
                except:
                    formatted_date = pub_date[:16] if len(pub_date) > 16 else pub_date
                    
                date_label = ctk.CTkLabel(
                    meta_frame,
                    text=f"🕒 {formatted_date}",
                    font=("Arial", 11),
                    text_color=("#718096", "#a0aec0")
                )
                date_label.pack(side="left", pady=2)
            
            # Source information
            source = article.get('author', 'Financial News')
            if source:
                source_label = ctk.CTkLabel(
                    meta_frame,
                    text=f"📰 {source}",
                    font=("Arial", 11),
                    text_color=("#718096", "#a0aec0")
                )
                source_label.pack(side="right", pady=2)

        # Add refresh button
        self.news_refresh_button = ctk.CTkButton(
            self.main_frame,
            text="🔄 Refresh Financial News",
            command=self.refresh_news,
            font=("Arial", 14, "bold"),
            height=40,
            corner_radius=20
        )
        self.news_refresh_button.pack(pady=20)
        self.news_articles.append(self.news_refresh_button)

    def refresh_news(self):
        """Refresh the financial news"""
        # Remove existing news articles only
        for article_widget in self.news_articles:
            try:
                article_widget.destroy()
            except:
                pass
        
        self.news_articles.clear()
        
        # Reload news
        self.load_news()

    def refresh_stock_data(self):
        """Refresh all stock and index data"""
        # Update stock widgets to show loading
        if hasattr(self, 'stock_widgets'):
            for symbol, widget_info in self.stock_widgets.items():
                widget_info['price_label'].configure(text="Updating...")
                widget_info['change_label'].configure(text="")
        
        # Update index widgets to show loading  
        if hasattr(self, 'index_widgets'):
            for symbol, widget_info in self.index_widgets.items():
                widget_info['value_label'].configure(text="Updating...")
                widget_info['change_label'].configure(text="")
        
        # Reload data in background
        threading.Thread(target=self.load_stock_data, daemon=True).start()
        threading.Thread(target=self.load_index_data, daemon=True).start()
        threading.Thread(target=self.load_chart_data, daemon=True).start()

    def show_error(self, error_message):
        """Display error message for financial news"""
        # Remove loading message if exists
        if hasattr(self, 'loading_label'):
            self.loading_label.destroy()
            
        error_label = ctk.CTkLabel(
            self.main_frame, 
            text=f"❌ {error_message}\n\n💡 Please check your internet connection and try again.", 
            font=("Arial", 14),
            text_color=("red", "#ff6b6b"),
            justify="center"
        )
        error_label.pack(pady=20)
        self.news_articles.append(error_label)
        
        # Add retry button
        retry_button = ctk.CTkButton(
            self.main_frame,
            text="🔄 Retry Loading Financial News",
            command=self.retry_load_news,
            font=("Arial", 12),
            height=35
        )
        retry_button.pack(pady=10)
        self.news_articles.append(retry_button)
    
    def retry_load_news(self):
        """Retry loading financial news"""
        # Remove existing news articles
        for article_widget in self.news_articles:
            try:
                article_widget.destroy()
            except:
                pass
        
        self.news_articles.clear()
        
        # Reload news
        self.load_news()

    def centring_the_app(self):
        width = 1000
        height = 700

        # get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")


if __name__ == "__main__":
    GUI()
