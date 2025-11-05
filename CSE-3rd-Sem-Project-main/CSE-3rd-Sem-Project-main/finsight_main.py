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
from config import theme_manager, COLORS

# Import custom modules
from sip_calculator import SIPCalculator
from currency_converter import CurrencyConverter

# Set initial appearance mode
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")
ctk.set_window_scaling(1.0)
ctk.set_widget_scaling(1.0)


class GUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Finsight - Enhanced Financial Hub")
        
        # Initialize news articles list for better refresh handling
        self.news_articles = []
        
        # Track current page for navigation highlighting
        self.current_page = "dashboard"

        # Configure window with enhanced styling
        self.setup_window()
        
        # Create enhanced navigation
        self.create_enhanced_navigation()

        # Main content frame with modern styling
        self.content_frame = ctk.CTkFrame(
            self.root, 
            corner_radius=20,
            fg_color=COLORS['surface'],
            border_width=1,
            border_color=COLORS['border']
        )
        self.content_frame.pack(pady=10, padx=15, fill="both", expand=True)

        # Show dashboard by default
        self.show_dashboard()

        self.root.mainloop()
    
    def setup_window(self):
        """Setup window with enhanced styling and responsive design"""
        # Configure window background first
        self.root.configure(fg_color=COLORS['background'])
        
        # Set window properties
        self.centring_the_app()
        
        # Enhanced window sizing with responsive design
        self.root.minsize(1200, 800)
        self.root.maxsize(1920, 1200)
        
        # Make window resizable
        self.root.resizable(True, True)
        
        # Ensure window is not maximized to show title bar properly
        self.root.wm_state('normal')
        
        # Add window icon if available (optional)
        try:
            self.root.iconbitmap("icon.ico")  # Add your icon file
        except:
            pass
        
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(0, weight=0)  # Navigation
        self.root.grid_rowconfigure(1, weight=1)  # Content
        self.root.grid_columnconfigure(0, weight=1)
    
    def create_enhanced_navigation(self):
        """Create enhanced navigation bar with modern design"""
        # Main navigation container
        nav_container = ctk.CTkFrame(
            self.root, 
            height=80,
            corner_radius=20,
            fg_color=COLORS['surface'],
            border_width=1,
            border_color=COLORS['border']
        )
        nav_container.pack(pady=(15, 5), padx=15, fill="x")
        nav_container.pack_propagate(False)
        
        # Left side - App branding
        left_frame = ctk.CTkFrame(nav_container, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=20)
        
        # App logo and title
        title_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        title_frame.pack(side="left", pady=15)
        
        # App icon
        app_icon = ctk.CTkLabel(
            title_frame,
            text="📊",
            font=("Segoe UI", 28)
        )
        app_icon.pack(side="left", padx=(0, 10))
        
        # App title with gradient effect
        title_label = ctk.CTkLabel(
            title_frame,
            text="Finsight",
            font=("Segoe UI", 24, "bold"),
            text_color=COLORS['primary']
        )
        title_label.pack(side="left")
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Financial Intelligence Hub",
            font=("Segoe UI", 11),
            text_color=COLORS['text_secondary']
        )
        subtitle_label.pack(side="left", padx=(10, 0), pady=(8, 0))
        
        # Center - Navigation buttons
        nav_center = ctk.CTkFrame(nav_container, fg_color="transparent")
        nav_center.pack(side="right", pady=15, padx=20)
        
        # Navigation button container
        nav_buttons_frame = ctk.CTkFrame(
            nav_center, 
            fg_color=COLORS['surface_elevated'],
            corner_radius=15,
            border_width=1,
            border_color=COLORS['border']
        )
        nav_buttons_frame.pack(side="left", padx=10)
        
        # Create navigation buttons with enhanced styling
        self.nav_buttons = {}
        
        button_configs = [
            ("dashboard", "🏠", "Dashboard", self.show_dashboard),
            ("sip", "💰", "SIP Calculator", self.show_sip_calculator),
            ("currency", "💱", "Currency", self.show_currency_converter)
        ]
        
        for i, (key, icon, text, command) in enumerate(button_configs):
            btn = ctk.CTkButton(
                nav_buttons_frame,
                text=f"{icon} {text}",
                command=command,
                width=140,
                height=40,
                font=("Segoe UI", 13, "bold"),
                corner_radius=12,
                fg_color="transparent",
                text_color=COLORS['text_secondary'],
                hover_color=COLORS['surface_elevated'],
                border_width=1,
                border_color=COLORS['border']  # Use solid color instead of transparent
            )
            btn.pack(side="left", padx=2, pady=8)
            self.nav_buttons[key] = btn
        
        # Right side - Theme toggle and settings
        right_frame = ctk.CTkFrame(nav_container, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=20)
        
        # Settings container
        settings_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        settings_frame.pack(side="right", pady=15)
        
        # Theme toggle button
        self.theme_btn = ctk.CTkButton(
            settings_frame,
            text="🌙" if theme_manager.current_theme == "light" else "☀️",
            command=self.toggle_theme,
            width=45,
            height=40,
            font=("Segoe UI", 16),
            corner_radius=12,
            fg_color=COLORS['surface_elevated'],
            hover_color=COLORS['primary'],
            border_width=1,
            border_color=COLORS['border']
        )
        self.theme_btn.pack(side="right", padx=5)
        
        # Settings button
        settings_btn = ctk.CTkButton(
            settings_frame,
            text="⚙️",
            command=self.show_settings,
            width=45,
            height=40,
            font=("Segoe UI", 16),
            corner_radius=12,
            fg_color=COLORS['surface_elevated'],
            hover_color=COLORS['primary'],
            border_width=1,
            border_color=COLORS['border']
        )
        settings_btn.pack(side="right", padx=5)
        
        # Update active navigation button
        self.update_nav_buttons()
    
    def update_nav_buttons(self):
        """Update navigation button states with smooth transitions"""
        for key, btn in self.nav_buttons.items():
            if key == self.current_page:
                # Active button styling with animation effect
                btn.configure(
                    fg_color=COLORS['primary'],
                    text_color="white",
                    hover_color=COLORS['primary_hover'],
                    border_width=2,
                    border_color=COLORS['primary']
                )
                # Add subtle scaling effect (simulated with padding)
                btn.pack_configure(pady=(6, 10))
            else:
                # Inactive button styling
                btn.configure(
                    fg_color="transparent",
                    text_color=COLORS['text_secondary'],
                    hover_color=COLORS['surface_elevated'],
                    border_width=1,
                    border_color=COLORS['border']  # Use a solid color instead of transparent
                )
                btn.pack_configure(pady=8)
    
    def animate_widget_entry(self, widget, delay=0):
        """Animate widget entry with fade and slide effect"""
        def show_widget():
            try:
                # Start with low opacity (simulated)
                widget.configure(fg_color=COLORS['surface'])
                # Add subtle entrance animation by configuring the widget
                widget.pack_configure(pady=(10, 10))
            except:
                pass
        
        # Schedule the animation
        self.root.after(delay, show_widget)
    
    def create_hover_effect(self, widget, normal_color, hover_color):
        """Create hover effect for widgets"""
        def on_enter(event):
            widget.configure(fg_color=hover_color)
        
        def on_leave(event):
            widget.configure(fg_color=normal_color)
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        new_theme = theme_manager.toggle_theme()
        
        # Update appearance mode
        ctk.set_appearance_mode("Dark" if new_theme == "dark" else "Light")
        
        # Update theme button icon
        self.theme_btn.configure(
            text="☀️" if new_theme == "dark" else "🌙"
        )
        
        # Refresh the current page to apply new theme
        if self.current_page == "dashboard":
            self.show_dashboard()
        elif self.current_page == "sip":
            self.show_sip_calculator()
        elif self.current_page == "currency":
            self.show_currency_converter()
    
    def show_settings(self):
        """Show settings dialog"""
        # Create settings window
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.configure(fg_color=COLORS['background'])
        
        # Center the settings window
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Settings content
        settings_label = ctk.CTkLabel(
            settings_window,
            text="⚙️ Settings",
            font=("Segoe UI", 20, "bold"),
            text_color=COLORS['text_primary']
        )
        settings_label.pack(pady=20)
        
        # Theme setting
        theme_frame = ctk.CTkFrame(settings_window, fg_color=COLORS['surface'])
        theme_frame.pack(pady=10, padx=20, fill="x")
        
        theme_label = ctk.CTkLabel(
            theme_frame,
            text="Theme Mode",
            font=("Segoe UI", 14),
            text_color=COLORS['text_primary']
        )
        theme_label.pack(pady=(15, 5))
        
        theme_switch = ctk.CTkSwitch(
            theme_frame,
            text="Dark Mode",
            command=self.toggle_theme,
            font=("Segoe UI", 12),
            text_color=COLORS['text_secondary']
        )
        theme_switch.pack(pady=(0, 15))
        
        if theme_manager.current_theme == "dark":
            theme_switch.select()
        
        # Close button
        close_btn = ctk.CTkButton(
            settings_window,
            text="Close",
            command=settings_window.destroy,
            font=("Segoe UI", 12),
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_hover']
        )
        close_btn.pack(pady=20)
    
    def clear_content(self):
        """Clear current content"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show main dashboard with enhanced design"""
        self.current_page = "dashboard"
        self.update_nav_buttons()
        self.clear_content()
        
        # Create enhanced scrollable main frame
        self.main_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            orientation="vertical",
            corner_radius=15,
            fg_color="transparent",
            scrollbar_button_color=COLORS['primary'],
            scrollbar_button_hover_color=COLORS['primary_hover']
        )
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.create_enhanced_greeting()
        self.create_enhanced_stock_widgets()
        self.load_enhanced_news()
    
    def show_sip_calculator(self):
        """Show SIP Calculator with enhanced theme"""
        self.current_page = "sip"
        self.update_nav_buttons()
        self.clear_content()
        
        # Create SIP calculator with enhanced theme
        sip_calculator = SIPCalculator(self.content_frame)
        sip_calculator.pack(fill="both", expand=True, padx=15, pady=15)
    
    def show_currency_converter(self):
        """Show Currency Converter with enhanced theme"""
        self.current_page = "currency"
        self.update_nav_buttons()
        self.clear_content()
        
        # Create currency converter with enhanced theme
        currency_converter = CurrencyConverter(self.content_frame)
        currency_converter.pack(fill="both", expand=True, padx=15, pady=15)

    def create_enhanced_greeting(self):
        """Create enhanced greeting section with better typography"""
        # Greeting container with modern design and enhanced visual hierarchy
        greeting_container = ctk.CTkFrame(
            self.main_frame,
            corner_radius=25,
            fg_color=COLORS['surface'],
            border_width=1,
            border_color=COLORS['border']
        )
        greeting_container.pack(pady=(0, 30), padx=25, fill="x")
        
        # Add subtle animation
        self.animate_widget_entry(greeting_container, 100)
        
        # Greeting content with enhanced layout
        current_time = time.strftime("%H:%M")
        current_hour = int(time.strftime("%H"))
        
        if 6 <= current_hour < 12:
            greeting = "Good Morning!"
            greeting_icon = "🌅"
            time_color = COLORS['warning']
        elif 12 <= current_hour < 17:
            greeting = "Good Afternoon!"
            greeting_icon = "☀️"
            time_color = COLORS['primary']
        elif 17 <= current_hour < 21:
            greeting = "Good Evening!"
            greeting_icon = "🌇"
            time_color = COLORS['secondary']
        else:
            greeting = "Working Late?"
            greeting_icon = "🌙"
            time_color = COLORS['accent']
        
        # Enhanced greeting header with better spacing
        greeting_header = ctk.CTkFrame(greeting_container, fg_color="transparent")
        greeting_header.pack(pady=35, padx=40, fill="x")
        
        # Icon and greeting with improved layout
        icon_label = ctk.CTkLabel(
            greeting_header,
            text=greeting_icon,
            font=("Segoe UI", 40)  # Larger icon for better visual impact
        )
        icon_label.pack(side="left")
        
        text_frame = ctk.CTkFrame(greeting_header, fg_color="transparent")
        text_frame.pack(side="left", padx=(20, 0), fill="x", expand=True)
        
        # Enhanced greeting text with better typography
        greeting_label = ctk.CTkLabel(
            text_frame,
            text=greeting,
            font=("Segoe UI", 32, "bold"),  # Larger font for hierarchy
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        greeting_label.pack(anchor="w")
        
        # Enhanced subtitle with better spacing
        subtitle_label = ctk.CTkLabel(
            text_frame,
            text="Welcome to Finsight - Your Complete Financial Intelligence Hub",
            font=("Segoe UI", 16, "normal"),  # Better font weight
            text_color=COLORS['text_secondary'],
            anchor="w"
        )
        subtitle_label.pack(anchor="w", pady=(8, 0))
        
        # Current time display with enhanced styling
        time_display = ctk.CTkFrame(
            greeting_header,
            fg_color=time_color,
            corner_radius=12,
            width=120,
            height=45
        )
        time_display.pack(side="right")
        time_display.pack_propagate(False)
        
        time_label = ctk.CTkLabel(
            time_display,
            text=f"🕐 {current_time}",
            font=("Segoe UI", 14, "bold"),
            text_color="white"
        )
        time_label.pack(pady=12)

    def create_enhanced_stock_widgets(self):
        """Create enhanced stock price widgets and market charts"""
        # Create main container for financial widgets with modern design
        financial_container = ctk.CTkFrame(
            self.main_frame,
            corner_radius=20,
            fg_color=COLORS['surface'],
            border_width=1,
            border_color=COLORS['border']
        )
        financial_container.pack(pady=20, padx=20, fill="x")
        
        # Enhanced title section
        title_section = ctk.CTkFrame(financial_container, fg_color="transparent")
        title_section.pack(pady=(20, 15), padx=25, fill="x")
        
        # Title with icon
        title_frame = ctk.CTkFrame(title_section, fg_color="transparent")
        title_frame.pack(side="left")
        
        title_icon = ctk.CTkLabel(
            title_frame,
            text="📈",
            font=("Segoe UI", 24)
        )
        title_icon.pack(side="left")
        
        title_text = ctk.CTkLabel(
            title_frame,
            text="Live Market Data & Charts",
            font=("Segoe UI", 20, "bold"),
            text_color=COLORS['text_primary']
        )
        title_text.pack(side="left", padx=(10, 0))
        
        # Live indicator
        live_indicator = ctk.CTkFrame(
            title_section,
            fg_color=COLORS['success'],
            corner_radius=15,
            width=80,
            height=25
        )
        live_indicator.pack(side="right")
        live_indicator.pack_propagate(False)
        
        live_label = ctk.CTkLabel(
            live_indicator,
            text="🔴 LIVE",
            font=("Segoe UI", 10, "bold"),
            text_color="white"
        )
        live_label.pack(pady=3)
        
        # Create enhanced market summary
        self.create_enhanced_market_summary(financial_container)
        
        # Create enhanced stock price widgets
        self.create_enhanced_stock_price_widgets(financial_container)
        
        # Create enhanced market chart
        self.create_enhanced_market_chart(financial_container)

    def create_enhanced_market_summary(self, parent):
        """Create enhanced market summary with major indices"""
        summary_frame = ctk.CTkFrame(
            parent,
            corner_radius=15,
            fg_color=COLORS['surface_elevated'],
            border_width=1,
            border_color=COLORS['border']
        )
        summary_frame.pack(pady=15, padx=25, fill="x")
        
        # Summary header
        summary_header = ctk.CTkFrame(summary_frame, fg_color="transparent")
        summary_header.pack(pady=(15, 10), padx=20, fill="x")
        
        summary_title = ctk.CTkLabel(
            summary_header,
            text="🏛️ Market Indices",
            font=("Segoe UI", 16, "bold"),
            text_color=COLORS['text_primary']
        )
        summary_title.pack(side="left")
        
        # Last updated time
        last_updated = ctk.CTkLabel(
            summary_header,
            text=f"Last updated: {datetime.now().strftime('%H:%M')}",
            font=("Segoe UI", 10),
            text_color=COLORS['text_tertiary']
        )
        last_updated.pack(side="right")
        
        # Create enhanced indices grid
        indices_grid = ctk.CTkFrame(summary_frame, fg_color="transparent")
        indices_grid.pack(pady=10, padx=15, fill="x")
        
        # Major market indices with enhanced design
        indices = {
            "^GSPC": {"name": "S&P 500", "icon": "🇺🇸"},
            "^DJI": {"name": "Dow Jones", "icon": "🏭"},
            "^IXIC": {"name": "NASDAQ", "icon": "💻"}
        }
        
        self.index_widgets = {}
        for i, (symbol, data) in enumerate(indices.items()):
            # Create enhanced index widget
            index_widget = ctk.CTkFrame(
                indices_grid,
                corner_radius=12,
                width=280,
                height=90,
                fg_color=COLORS['card_bg'],
                border_width=1,
                border_color=COLORS['card_border']
            )
            index_widget.grid(row=0, column=i, padx=8, pady=10, sticky="ew")
            index_widget.grid_propagate(False)
            
            # Index header with flag and name
            header_frame = ctk.CTkFrame(index_widget, fg_color="transparent")
            header_frame.pack(pady=(12, 5), padx=15, fill="x")
            
            icon_label = ctk.CTkLabel(
                header_frame,
                text=data["icon"],
                font=("Segoe UI", 16)
            )
            icon_label.pack(side="left")
            
            name_label = ctk.CTkLabel(
                header_frame,
                text=data["name"],
                font=("Segoe UI", 13, "bold"),
                text_color=COLORS['text_primary']
            )
            name_label.pack(side="left", padx=(8, 0))
            
            # Index value with larger font
            value_label = ctk.CTkLabel(
                index_widget,
                text="Loading...",
                font=("Segoe UI", 18, "bold"),
                text_color=COLORS['text_primary']
            )
            value_label.pack(pady=(0, 2))
            
            # Index change with color coding
            change_label = ctk.CTkLabel(
                index_widget,
                text="",
                font=("Segoe UI", 11, "bold")
            )
            change_label.pack(pady=(0, 12))
            
            self.index_widgets[symbol] = {
                'value_label': value_label,
                'change_label': change_label,
                'widget': index_widget
            }
        
        # Configure grid weights
        for i in range(3):
            indices_grid.grid_columnconfigure(i, weight=1)
        
        # Load index data
        threading.Thread(target=self.load_enhanced_index_data, daemon=True).start()

    def load_enhanced_index_data(self):
        """Load market indices data with enhanced error handling"""
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
                                       self.update_enhanced_index_widget(s, v, c))
                        
                except Exception as e:
                    print(f"Error loading index {symbol}: {e}")
                    self.root.after(0, lambda s=symbol: 
                                   self.update_enhanced_index_widget(s, "Error", 0))
                    
        except Exception as e:
            print(f"Error in load_enhanced_index_data: {e}")

    def update_enhanced_index_widget(self, symbol, value, change_percent):
        """Update market index widget with enhanced styling"""
        if symbol in self.index_widgets:
            widget_info = self.index_widgets[symbol]
            
            # Update value with better formatting
            if isinstance(value, (int, float)):
                if value >= 1000:
                    value_text = f"{value:,.0f}"
                else:
                    value_text = f"{value:.2f}"
                widget_info['value_label'].configure(text=value_text)
            else:
                widget_info['value_label'].configure(
                    text=str(value),
                    text_color=COLORS['error']
                )
            
            # Update change with enhanced styling
            if isinstance(change_percent, (int, float)) and change_percent != 0:
                change_text = f"{abs(change_percent):.2f}%"
                if change_percent > 0:
                    color = COLORS['success']
                    arrow = "▲"
                    bg_color = COLORS['success_bg']
                else:
                    color = COLORS['error']
                    arrow = "▼"
                    bg_color = COLORS['error_bg']
                
                widget_info['change_label'].configure(
                    text=f"{arrow} {change_text}",
                    text_color=color
                )
                
                # Add subtle background color to widget for positive/negative
                widget_info['widget'].configure(
                    border_color=color,
                    border_width=2
                )
            else:
                widget_info['change_label'].configure(
                    text="--",
                    text_color=COLORS['text_tertiary']
                )

    def create_enhanced_stock_price_widgets(self, parent):
        """Create enhanced live stock price widgets"""
        # Stock widgets container with better design
        stock_container = ctk.CTkFrame(
            parent,
            corner_radius=15,
            fg_color=COLORS['surface_elevated'],
            border_width=1,
            border_color=COLORS['border']
        )
        stock_container.pack(pady=15, padx=25, fill="x")
        
        # Stock section header
        stock_header = ctk.CTkFrame(stock_container, fg_color="transparent")
        stock_header.pack(pady=(15, 10), padx=20, fill="x")
        
        stock_title = ctk.CTkLabel(
            stock_header,
            text="💰 Popular Stocks",
            font=("Segoe UI", 16, "bold"),
            text_color=COLORS['text_primary']
        )
        stock_title.pack(side="left")
        
        # Refresh button with better design
        refresh_stocks_btn = ctk.CTkButton(
            stock_header,
            text="🔄 Refresh",
            command=self.refresh_enhanced_stock_data,
            font=("Segoe UI", 11),
            height=30,
            width=90,
            fg_color="transparent",
            text_color=COLORS['primary'],
            hover_color=COLORS['surface'],
            border_width=1,
            border_color=COLORS['primary'],
            corner_radius=8
        )
        refresh_stocks_btn.pack(side="right")
        
        # Create enhanced stocks grid
        stocks_grid = ctk.CTkFrame(stock_container, fg_color="transparent")
        stocks_grid.pack(pady=10, padx=15, fill="x")
        
        # Enhanced popular stocks with company info
        popular_stocks = {
            "AAPL": {"name": "Apple Inc.", "icon": "🍎"},
            "GOOGL": {"name": "Alphabet Inc.", "icon": "🔍"},
            "MSFT": {"name": "Microsoft Corp.", "icon": "🪟"},
            "TSLA": {"name": "Tesla Inc.", "icon": "🚗"},
            "AMZN": {"name": "Amazon.com Inc.", "icon": "📦"},
            "NVDA": {"name": "NVIDIA Corp.", "icon": "🎮"}
        }
        
        # Create enhanced stock widgets in a grid (3 columns, 2 rows)
        self.stock_widgets = {}
        for i, (symbol, data) in enumerate(popular_stocks.items()):
            row = i // 3
            col = i % 3
            
            # Create enhanced individual stock widget
            stock_widget = ctk.CTkFrame(
                stocks_grid,
                corner_radius=12,
                width=260,
                height=100,
                fg_color=COLORS['card_bg'],
                border_width=1,
                border_color=COLORS['card_border']
            )
            stock_widget.grid(row=row, column=col, padx=8, pady=8, sticky="ew")
            stock_widget.grid_propagate(False)
            
            # Stock header with icon and symbol
            stock_widget_header = ctk.CTkFrame(stock_widget, fg_color="transparent")
            stock_widget_header.pack(pady=(12, 5), padx=15, fill="x")
            
            # Company icon
            icon_label = ctk.CTkLabel(
                stock_widget_header,
                text=data["icon"],
                font=("Segoe UI", 18)
            )
            icon_label.pack(side="left")
            
            # Symbol and company name
            symbol_frame = ctk.CTkFrame(stock_widget_header, fg_color="transparent")
            symbol_frame.pack(side="left", padx=(10, 0), fill="x", expand=True)
            
            symbol_label = ctk.CTkLabel(
                symbol_frame,
                text=symbol,
                font=("Segoe UI", 14, "bold"),
                text_color=COLORS['primary'],
                anchor="w"
            )
            symbol_label.pack(anchor="w")
            
            company_label = ctk.CTkLabel(
                symbol_frame,
                text=data["name"],
                font=("Segoe UI", 9),
                text_color=COLORS['text_tertiary'],
                anchor="w"
            )
            company_label.pack(anchor="w")
            
            # Price section
            price_frame = ctk.CTkFrame(stock_widget, fg_color="transparent")
            price_frame.pack(pady=(0, 5), padx=15, fill="x")
            
            # Price label with larger font
            price_label = ctk.CTkLabel(
                price_frame,
                text="Loading...",
                font=("Segoe UI", 16, "bold"),
                text_color=COLORS['text_primary'],
                anchor="w"
            )
            price_label.pack(side="left")
            
            # Change label with trend indicator
            change_label = ctk.CTkLabel(
                price_frame,
                text="",
                font=("Segoe UI", 11, "bold"),
                anchor="e"
            )
            change_label.pack(side="right")
            
            self.stock_widgets[symbol] = {
                'price_label': price_label,
                'change_label': change_label,
                'widget': stock_widget
            }
        
        # Configure grid weights
        for i in range(3):
            stocks_grid.grid_columnconfigure(i, weight=1)
        
        # Load stock data in background
        threading.Thread(target=self.load_enhanced_stock_data, daemon=True).start()

    def create_enhanced_market_chart(self, parent):
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

    def load_enhanced_stock_data(self):
        """Load real-time stock data with enhanced error handling"""
        try:
            for symbol in self.stock_widgets.keys():
                try:
                    # Get stock info with better error handling
                    stock = yf.Ticker(symbol)
                    hist = stock.history(period="2d")
                    
                    if not hist.empty and len(hist) >= 2:
                        current_price = hist['Close'].iloc[-1]
                        prev_price = hist['Close'].iloc[-2]
                        change = current_price - prev_price
                        change_percent = (change / prev_price) * 100
                        
                        # Update UI in main thread
                        self.root.after(0, lambda s=symbol, p=current_price, c=change_percent: 
                                       self.update_enhanced_stock_widget(s, p, c))
                    else:
                        # Fallback to basic info
                        info = stock.info
                        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
                        if current_price:
                            self.root.after(0, lambda s=symbol, p=current_price: 
                                           self.update_enhanced_stock_widget(s, p, 0))
                        else:
                            self.root.after(0, lambda s=symbol: 
                                           self.update_enhanced_stock_widget(s, "N/A", 0))
                        
                except Exception as e:
                    print(f"Error loading {symbol}: {e}")
                    self.root.after(0, lambda s=symbol: 
                                   self.update_enhanced_stock_widget(s, "Error", 0))
                    
        except Exception as e:
            print(f"Error in load_enhanced_stock_data: {e}")

    def update_enhanced_stock_widget(self, symbol, price, change_percent):
        """Update individual stock widget with enhanced styling"""
        if symbol in self.stock_widgets:
            widget_info = self.stock_widgets[symbol]
            
            # Update price with better formatting
            if isinstance(price, (int, float)):
                if price >= 1000:
                    price_text = f"${price:,.0f}"
                else:
                    price_text = f"${price:.2f}"
                widget_info['price_label'].configure(
                    text=price_text,
                    text_color=COLORS['text_primary']
                )
            else:
                widget_info['price_label'].configure(
                    text=str(price),
                    text_color=COLORS['error']
                )
            
            # Update change with enhanced styling
            if isinstance(change_percent, (int, float)) and change_percent != 0:
                change_text = f"{abs(change_percent):.2f}%"
                if change_percent > 0:
                    color = COLORS['success']
                    arrow = "▲"
                    border_color = COLORS['success']
                else:
                    color = COLORS['error']
                    arrow = "▼"
                    border_color = COLORS['error']
                
                widget_info['change_label'].configure(
                    text=f"{arrow} {change_text}",
                    text_color=color
                )
                
                # Add subtle border color indication
                widget_info['widget'].configure(
                    border_color=border_color,
                    border_width=2
                )
            else:
                widget_info['change_label'].configure(
                    text="--",
                    text_color=COLORS['text_tertiary']
                )
                widget_info['widget'].configure(
                    border_color=COLORS['card_border'],
                    border_width=1
                )

    def refresh_enhanced_stock_data(self):
        """Refresh all stock and index data with loading states"""
        # Update stock widgets to show loading
        if hasattr(self, 'stock_widgets'):
            for symbol, widget_info in self.stock_widgets.items():
                widget_info['price_label'].configure(
                    text="🔄 Updating...",
                    text_color=COLORS['text_secondary']
                )
                widget_info['change_label'].configure(text="")
                widget_info['widget'].configure(
                    border_color=COLORS['card_border'],
                    border_width=1
                )
        
        # Update index widgets to show loading  
        if hasattr(self, 'index_widgets'):
            for symbol, widget_info in self.index_widgets.items():
                widget_info['value_label'].configure(
                    text="🔄 Updating...",
                    text_color=COLORS['text_secondary']
                )
                widget_info['change_label'].configure(text="")
                widget_info['widget'].configure(
                    border_color=COLORS['card_border'],
                    border_width=1
                )
        
        # Reload data in background
        threading.Thread(target=self.load_enhanced_stock_data, daemon=True).start()
        threading.Thread(target=self.load_enhanced_index_data, daemon=True).start()
        threading.Thread(target=self.load_enhanced_chart_data, daemon=True).start()

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

    def load_enhanced_news(self):
        """Load enhanced financial news articles in a separate thread"""
        # Enhanced loading message with modern design
        loading_container = ctk.CTkFrame(
            self.main_frame,
            corner_radius=20,
            fg_color=COLORS['surface'],
            border_width=1,
            border_color=COLORS['border']
        )
        loading_container.pack(pady=20, padx=20, fill="x")
        
        # Loading content
        loading_content = ctk.CTkFrame(loading_container, fg_color="transparent")
        loading_content.pack(pady=30, padx=30)
        
        # Loading icon and text
        loading_frame = ctk.CTkFrame(loading_content, fg_color="transparent")
        loading_frame.pack()
        
        loading_icon = ctk.CTkLabel(
            loading_frame,
            text="📰",
            font=("Segoe UI", 32)
        )
        loading_icon.pack(side="left")
        
        self.loading_label = ctk.CTkLabel(
            loading_frame,
            text="Loading latest financial news & market updates...",
            font=("Segoe UI", 16, "bold"),
            text_color=COLORS['text_primary']
        )
        self.loading_label.pack(side="left", padx=(15, 0))
        
        # Progress indicator
        progress_label = ctk.CTkLabel(
            loading_content,
            text="🔄 Fetching from multiple sources",
            font=("Segoe UI", 12),
            text_color=COLORS['text_secondary']
        )
        progress_label.pack(pady=(10, 0))
        
        self.news_articles.append(loading_container)
        
        # Fetch news in background thread to prevent UI freezing
        threading.Thread(target=self.fetch_and_display_enhanced_news, daemon=True).start()

    def fetch_and_display_enhanced_news(self):
        """Fetch financial/stock news from API and display in enhanced UI"""
        try:
            # Using MarketWatch RSS feed (verified working)
            marketwatch_url = "https://api.rss2json.com/v1/api.json?rss_url=https://feeds.marketwatch.com/marketwatch/realtimeheadlines/"
            
            response = requests.get(marketwatch_url, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'ok':
                    # Schedule UI update in main thread
                    self.root.after(0, lambda: self.display_enhanced_financial_news(data))
                else:
                    self.root.after(0, lambda: self.show_enhanced_error("Failed to retrieve financial news data"))
            else:
                self.root.after(0, lambda: self.show_enhanced_error(f"API returned status code: {response.status_code}"))
                
        except requests.exceptions.Timeout:
            self.root.after(0, lambda: self.show_enhanced_error("Request timed out. Please check your internet connection."))
        except requests.exceptions.ConnectionError:
            self.root.after(0, lambda: self.show_enhanced_error("Connection error. Please check your internet connection."))
        except Exception as e:
            self.root.after(0, lambda: self.show_enhanced_error(f"Error fetching financial news: {str(e)}"))

    def display_enhanced_financial_news(self, data):
        """Display financial news articles in enhanced UI"""
        # Remove loading message
        for widget in self.news_articles:
            try:
                widget.destroy()
            except:
                pass
        self.news_articles.clear()
        
        # Enhanced financial news container
        news_container = ctk.CTkFrame(
            self.main_frame,
            corner_radius=20,
            fg_color=COLORS['surface'],
            border_width=1,
            border_color=COLORS['border']
        )
        news_container.pack(pady=20, padx=20, fill="x")
        self.news_articles.append(news_container)
        
        # Enhanced news header
        news_header = ctk.CTkFrame(news_container, fg_color="transparent")
        news_header.pack(pady=(20, 15), padx=25, fill="x")
        
        # Header left side
        header_left = ctk.CTkFrame(news_header, fg_color="transparent")
        header_left.pack(side="left", fill="x", expand=True)
        
        # News icon and title
        title_frame = ctk.CTkFrame(header_left, fg_color="transparent")
        title_frame.pack(side="left")
        
        news_icon = ctk.CTkLabel(
            title_frame,
            text="📰",
            font=("Segoe UI", 24)
        )
        news_icon.pack(side="left")
        
        news_title = ctk.CTkLabel(
            title_frame,
            text="Latest Financial News",
            font=("Segoe UI", 20, "bold"),
            text_color=COLORS['text_primary']
        )
        news_title.pack(side="left", padx=(10, 0))
        
        # News subtitle
        news_subtitle = ctk.CTkLabel(
            header_left,
            text="Real-time market updates and financial insights",
            font=("Segoe UI", 12),
            text_color=COLORS['text_secondary']
        )
        news_subtitle.pack(side="left", padx=(45, 0), pady=(5, 0))
        
        # Header right side - refresh button
        refresh_news_btn = ctk.CTkButton(
            news_header,
            text="🔄 Refresh",
            command=self.refresh_enhanced_news,
            font=("Segoe UI", 11),
            height=30,
            width=90,
            fg_color="transparent",
            text_color=COLORS['primary'],
            hover_color=COLORS['surface'],
            border_width=1,
            border_color=COLORS['primary'],
            corner_radius=8
        )
        refresh_news_btn.pack(side="right")
        
        # News articles container
        articles_container = ctk.CTkFrame(news_container, fg_color="transparent")
        articles_container.pack(pady=(10, 20), padx=20, fill="x")
        
        # Display enhanced news articles
        articles = data.get('items', [])[:6]  # Show top 6 financial articles
        
        for i, article in enumerate(articles):
            # Create enhanced frame for each article
            article_frame = ctk.CTkFrame(
                articles_container,
                corner_radius=15,
                fg_color=COLORS['card_bg'],
                border_width=1,
                border_color=COLORS['card_border']
            )
            article_frame.pack(pady=8, padx=10, fill="x")
            
            # Article content
            article_content = ctk.CTkFrame(article_frame, fg_color="transparent")
            article_content.pack(pady=15, padx=20, fill="x")
            
            # Article title with better formatting
            title = article.get('title', 'No title')
            if len(title) > 120:
                title = title[:120] + "..."
                
            title_label = ctk.CTkLabel(
                article_content,
                text=title,
                font=("Segoe UI", 15, "bold"),
                wraplength=750,
                justify="left",
                text_color=COLORS['text_primary'],
                anchor="w"
            )
            title_label.pack(anchor="w", pady=(0, 8))
            
            # Article description with better formatting
            description = article.get('description', '') or article.get('content', '')
            if not description:
                description = "Click to read full article..."
            
            # Clean up description (remove HTML tags)
            description = re.sub(r'<[^>]+>', '', description)
            if len(description) > 200:
                description = description[:200] + "..."
                
            desc_label = ctk.CTkLabel(
                article_content,
                text=description,
                font=("Segoe UI", 12),
                wraplength=750,
                justify="left",
                text_color=COLORS['text_secondary'],
                anchor="w"
            )
            desc_label.pack(anchor="w", pady=(0, 10))
            
            # Enhanced metadata frame
            meta_frame = ctk.CTkFrame(article_content, fg_color="transparent")
            meta_frame.pack(fill="x")
            
            # Publication date with better formatting
            pub_date = article.get('pubDate', '')
            if pub_date:
                try:
                    if 'T' in pub_date:
                        date_obj = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                    else:
                        date_obj = datetime.strptime(pub_date[:19], "%Y-%m-%d %H:%M:%S")
                    
                    formatted_date = date_obj.strftime("%b %d, %Y • %I:%M %p")
                except:
                    formatted_date = pub_date[:16] if len(pub_date) > 16 else pub_date
                    
                date_frame = ctk.CTkFrame(meta_frame, fg_color=COLORS['surface_elevated'], corner_radius=8)
                date_frame.pack(side="left")
                
                date_label = ctk.CTkLabel(
                    date_frame,
                    text=f"🕒 {formatted_date}",
                    font=("Segoe UI", 10),
                    text_color=COLORS['text_tertiary']
                )
                date_label.pack(padx=8, pady=4)
            
            # Source information with better styling
            source = article.get('author', 'Financial News')
            if source:
                source_frame = ctk.CTkFrame(meta_frame, fg_color=COLORS['surface_elevated'], corner_radius=8)
                source_frame.pack(side="right")
                
                source_label = ctk.CTkLabel(
                    source_frame,
                    text=f"� {source}",
                    font=("Segoe UI", 10),
                    text_color=COLORS['text_tertiary']
                )
                source_label.pack(padx=8, pady=4)

    def show_enhanced_error(self, error_message):
        """Display enhanced error message for financial news"""
        # Remove loading message if exists
        for widget in self.news_articles:
            try:
                widget.destroy()
            except:
                pass
        self.news_articles.clear()
        
        # Enhanced error container
        error_container = ctk.CTkFrame(
            self.main_frame,
            corner_radius=20,
            fg_color=COLORS['surface'],
            border_width=2,
            border_color=COLORS['error']
        )
        error_container.pack(pady=20, padx=20, fill="x")
        self.news_articles.append(error_container)
        
        # Error content
        error_content = ctk.CTkFrame(error_container, fg_color="transparent")
        error_content.pack(pady=30, padx=30)
        
        # Error icon and message
        error_frame = ctk.CTkFrame(error_content, fg_color="transparent")
        error_frame.pack()
        
        error_icon = ctk.CTkLabel(
            error_frame,
            text="❌",
            font=("Segoe UI", 32)
        )
        error_icon.pack(side="left")
        
        error_label = ctk.CTkLabel(
            error_frame,
            text=f"News Loading Error",
            font=("Segoe UI", 18, "bold"),
            text_color=COLORS['error']
        )
        error_label.pack(side="left", padx=(15, 0))
        
        # Error details
        error_details = ctk.CTkLabel(
            error_content,
            text=f"{error_message}\n\nPlease check your internet connection and try again.",
            font=("Segoe UI", 12),
            text_color=COLORS['text_secondary'],
            justify="center"
        )
        error_details.pack(pady=(15, 20))
        
        # Enhanced retry button
        retry_button = ctk.CTkButton(
            error_content,
            text="🔄 Retry Loading News",
            command=self.retry_enhanced_news,
            font=("Segoe UI", 12, "bold"),
            height=40,
            fg_color=COLORS['primary'],
            hover_color=COLORS['primary_hover'],
            corner_radius=10
        )
        retry_button.pack()
    
    def refresh_enhanced_news(self):
        """Refresh the enhanced financial news"""
        # Remove existing news articles
        for article_widget in self.news_articles:
            try:
                article_widget.destroy()
            except:
                pass
        
        self.news_articles.clear()
        
        # Reload enhanced news
        self.load_enhanced_news()
    
    def retry_enhanced_news(self):
        """Retry loading enhanced financial news"""
        self.refresh_enhanced_news()

    def centring_the_app(self):
        width = 1000
        height = 700

        # get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")


    def centring_the_app(self):
        """Center the application window on screen with enhanced sizing"""
        # Enhanced window dimensions for better experience
        width = 1400
        height = 900

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate center position with title bar consideration
        x = (screen_width - width) // 2
        y = max(50, (screen_height - height) // 2 - 50)  # Ensure title bar is visible

        # Set geometry and configure window
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Make window resizable but set minimum size
        self.root.minsize(1200, 800)


if __name__ == "__main__":
    GUI()
